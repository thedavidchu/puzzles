#!/usr/bin/env python3
"""
Asymmetric encryption/decryption with compression

This module provides functionality to compress/decompress and encrypt/decrypt files using RSA keys.
It can:
- Generate keys: generate the public and private RSA keys
- Encrypt: compress input file with gzip, encrypt with RSA public key
- Decrypt: decrypt with RSA private key, decompress with gzip
"""

import argparse
import base64
import binascii
import getpass
import gzip
import os
import struct
import sys
from pathlib import Path

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding, rsa
    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
except ImportError:
    print("Error: cryptography package required. Install with: pip install cryptography", file=sys.stderr)
    sys.exit(1)


def get_password(prompt: str = "Enter password: ", confirm: bool = False) -> bytes:
    """Get password from user input.
    
    Args:
        prompt: Prompt message to display
        confirm: Whether to ask for password confirmation
        
    Returns:
        Password as bytes
        
    Raises:
        SystemExit: If passwords don't match during confirmation
    """
    password = getpass.getpass(prompt)
    
    if confirm:
        confirm_password = getpass.getpass("Confirm password: ")
        if password != confirm_password:
            print("Error: Passwords do not match", file=sys.stderr)
            sys.exit(1)
    
    return password.encode('utf-8')


def read_file(file_path: str | Path) -> bytes:
    """Read file contents as bytes.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File contents as bytes
        
    Raises:
        SystemExit: If file not found or read error occurs
    """
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{file_path}' not found", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading file '{file_path}'", file=sys.stderr)
        sys.exit(1)
    except IsADirectoryError:
        print(f"Error: '{file_path}' is a directory, not a file", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)


def write_file(file_path: str | Path, data: bytes) -> None:
    """Write bytes data to file.
    
    Args:
        file_path: Path to the output file
        data: Bytes data to write
        
    Raises:
        SystemExit: If write error occurs
    """
    try:
        with open(file_path, 'wb') as f:
            f.write(data)
    except PermissionError:
        print(f"Error: Permission denied writing to file '{file_path}'", file=sys.stderr)
        sys.exit(1)
    except IsADirectoryError:
        print(f"Error: '{file_path}' is a directory, not a file", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)


def write_text_file(file_path: str | Path, text: str) -> None:
    """Write text data to file.
    
    Args:
        file_path: Path to the output file
        text: Text data to write
        
    Raises:
        SystemExit: If write error occurs
    """
    try:
        with open(file_path, 'w') as f:
            f.write(text)
    except PermissionError:
        print(f"Error: Permission denied writing to file '{file_path}'", file=sys.stderr)
        sys.exit(1)
    except IsADirectoryError:
        print(f"Error: '{file_path}' is a directory, not a file", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)


def read_text_file(file_path: str | Path) -> str:
    """Read file contents as text.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        File contents as string
        
    Raises:
        SystemExit: If file not found or read error occurs
    """
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{file_path}' not found", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading file '{file_path}'", file=sys.stderr)
        sys.exit(1)
    except IsADirectoryError:
        print(f"Error: '{file_path}' is a directory, not a file", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Error: File '{file_path}' is not a valid text file: {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)


def load_public_key(key_file_path: str | Path) -> RSAPublicKey:
    """Load RSA public key from PEM file.
    
    Args:
        key_file_path: Path to the PEM public key file
        
    Returns:
        RSA public key object
        
    Raises:
        SystemExit: If key file not found or invalid
        ValueError: If key file doesn't contain RSA public key
    """
    try:
        with open(key_file_path, 'rb') as f:
            key_data = f.read()
        public_key = load_pem_public_key(key_data)
        if not isinstance(public_key, RSAPublicKey):
            raise ValueError("Key file does not contain an RSA public key")
        return public_key
    except FileNotFoundError:
        print(f"Error: Public key file '{key_file_path}' not found", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading key file '{key_file_path}'", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid public key format: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error loading public key: {e}", file=sys.stderr)
        sys.exit(1)


def load_private_key(key_file_path: str | Path, password: bytes | None = None) -> RSAPrivateKey:
    """Load RSA private key from PEM file.
    
    Args:
        key_file_path: Path to the PEM private key file
        password: Password to decrypt the private key (None if not encrypted)
        
    Returns:
        RSA private key object
        
    Raises:
        SystemExit: If key file not found, invalid, or wrong password
        ValueError: If key file doesn't contain RSA private key
    """
    try:
        with open(key_file_path, 'rb') as f:
            key_data = f.read()
        private_key = load_pem_private_key(key_data, password=password)
        if not isinstance(private_key, RSAPrivateKey):
            raise ValueError("Key file does not contain an RSA private key")
        return private_key
    except FileNotFoundError:
        print(f"Error: Private key file '{key_file_path}' not found", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading key file '{key_file_path}'", file=sys.stderr)
        sys.exit(1)
    except TypeError:
        print("Error: Private key is encrypted but no password provided", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        if "Could not deserialize key data" in str(e) or "Invalid password" in str(e):
            print("Error: Invalid password for encrypted private key", file=sys.stderr)
        else:
            print(f"Error: Invalid private key format: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error loading private key: {e}", file=sys.stderr)
        sys.exit(1)


def generate_aes_key() -> bytes:
    """Generate a random AES-256 key.
    
    Returns:
        32-byte AES key
    """
    return os.urandom(32)


def encrypt_aes(data: bytes, key: bytes) -> bytes:
    """Encrypt data using AES-256-GCM.
    
    Args:
        data: Data to encrypt
        key: 32-byte AES key
        
    Returns:
        IV + encrypted data + auth tag (concatenated)
    """
    iv = os.urandom(12)  # 96-bit IV for GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return iv + ciphertext + encryptor.tag


def decrypt_aes(encrypted_data: bytes, key: bytes) -> bytes:
    """Decrypt AES-256-GCM encrypted data.
    
    Args:
        encrypted_data: IV + encrypted data + auth tag (concatenated)
        key: 32-byte AES key
        
    Returns:
        Decrypted data
        
    Raises:
        Exception: If decryption or authentication fails
    """
    if len(encrypted_data) < 28:  # 12-byte IV + 16-byte tag minimum
        raise ValueError("Encrypted data too short")
    
    iv = encrypted_data[:12]
    ciphertext = encrypted_data[12:-16]
    tag = encrypted_data[-16:]
    
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def compress_data(data: bytes) -> bytes:
    """Compress data using gzip.
    
    Args:
        data: Bytes data to compress
        
    Returns:
        Compressed data as bytes
    """
    return gzip.compress(data)


def decompress_data(data: bytes) -> bytes:
    """Decompress data using gzip.
    
    Args:
        data: Compressed bytes data
        
    Returns:
        Decompressed data as bytes
        
    Raises:
        SystemExit: If decompression fails
    """
    try:
        return gzip.decompress(data)
    except gzip.BadGzipFile:
        print("Error: Invalid gzip data format", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error decompressing data: {e}", file=sys.stderr)
        sys.exit(1)


def encrypt_data(data: bytes, public_key: RSAPublicKey) -> bytes:
    """Encrypt data using hybrid encryption (AES + RSA).
    
    Uses AES-256-GCM for data encryption and RSA-OAEP for key encryption.
    This allows encryption of arbitrarily large data.
    
    Args:
        data: Bytes data to encrypt
        public_key: RSA public key for encrypting the AES key
        
    Returns:
        Encrypted data as bytes (format: encrypted_aes_key_length + encrypted_aes_key + encrypted_data)
        
    Raises:
        SystemExit: If encryption fails
    """
    try:
        # Generate a random AES key
        aes_key = generate_aes_key()
        
        # Encrypt the data with AES
        encrypted_data = encrypt_aes(data, aes_key)
        
        # Encrypt the AES key with RSA
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Combine: encrypted_aes_key_length (4 bytes) + encrypted_aes_key + encrypted_data
        result = struct.pack('<I', len(encrypted_aes_key)) + encrypted_aes_key + encrypted_data
        return result
            
    except ValueError as e:
        print(f"Error: Encryption failed - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error encrypting data: {e}", file=sys.stderr)
        sys.exit(1)


def decrypt_data(encrypted_data: bytes, private_key: RSAPrivateKey) -> bytes:
    """Decrypt data using hybrid decryption (RSA + AES).
    
    Expects data format: encrypted_aes_key_length + encrypted_aes_key + encrypted_data
    
    Args:
        encrypted_data: Hybrid encrypted bytes data
        private_key: RSA private key for decrypting the AES key
        
    Returns:
        Decrypted data as bytes
        
    Raises:
        SystemExit: If decryption fails
    """
    try:
        # Check minimum size (4 bytes for length + some encrypted key + some data)
        if len(encrypted_data) < 8:
            raise ValueError("Encrypted data too short for hybrid format")
        
        # Extract encrypted AES key length
        aes_key_length = struct.unpack('<I', encrypted_data[:4])[0]
        
        # Validate the length
        if aes_key_length <= 0 or aes_key_length > len(encrypted_data) - 4:
            raise ValueError("Invalid encrypted AES key length")
        
        # Extract encrypted AES key and encrypted data
        encrypted_aes_key = encrypted_data[4:4+aes_key_length]
        encrypted_aes_data = encrypted_data[4+aes_key_length:]
        
        # Decrypt the AES key with RSA
        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Decrypt the data with AES
        decrypted_data = decrypt_aes(encrypted_aes_data, aes_key)
        return decrypted_data
        
    except struct.error as e:
        print(f"Error: Invalid data format - {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        if "Invalid password" in str(e) or "Could not deserialize" in str(e):
            print(f"Error: Decryption failed - invalid key or corrupted data: {e}", file=sys.stderr)
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error decrypting data: {e}", file=sys.stderr)
        sys.exit(1)


def generate_key_pair(key_size: int = 2048) -> tuple[RSAPrivateKey, RSAPublicKey]:
    """Generate RSA key pair.
    
    Args:
        key_size: RSA key size in bits (default: 2048)
        
    Returns:
        Tuple of (private_key, public_key)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    public_key = private_key.public_key()
    return private_key, public_key


def save_private_key(private_key: RSAPrivateKey, filename: str | Path, password: bytes | None = None) -> None:
    """Save private key to PEM file.
    
    Args:
        private_key: RSA private key to save
        filename: Path to save the private key file
        password: Password to encrypt the private key (None for no encryption)
    """
    if password:
        encryption_algorithm = serialization.BestAvailableEncryption(password)
    else:
        encryption_algorithm = serialization.NoEncryption()
    
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm
    )
    
    with open(filename, 'wb') as f:
        f.write(pem)


def save_public_key(public_key: RSAPublicKey, filename: str | Path) -> None:
    """Save public key to PEM file.
    
    Args:
        public_key: RSA public key to save
        filename: Path to save the public key file
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    with open(filename, 'wb') as f:
        f.write(pem)


def generate_keys_mode(args: argparse.Namespace) -> None:
    """Handle key generation mode."""
    private_key_path = Path(args.private_key)
    public_key_path = Path(args.public_key)
    
    print(f"Generating RSA key pair ({args.key_size} bits)...")
    private_key, public_key = generate_key_pair(args.key_size)
    
    # Get password for private key encryption
    password = None
    if not args.no_password:
        print("\nEnter a password to protect the private key (press Enter for no password):")
        password_input = getpass.getpass("Password: ")
        if password_input:
            confirm_password = getpass.getpass("Confirm password: ")
            if password_input != confirm_password:
                print("Error: Passwords do not match", file=sys.stderr)
                sys.exit(1)
            password = password_input.encode('utf-8')
            print("Private key will be encrypted with password")
        else:
            print("Private key will be saved without password protection")
    
    print(f"Saving private key to: {private_key_path}")
    save_private_key(private_key, private_key_path, password)
    
    print(f"Saving public key to: {public_key_path}")
    save_public_key(public_key, public_key_path)
    
    print("Key generation complete!")
    print(f"Public key: {public_key_path}")
    print(f"Private key: {private_key_path}")
    if password:
        print("Note: Private key is password protected")


def encrypt_mode(args: argparse.Namespace) -> None:
    """Handle encryption mode."""
    # Validate input files exist
    input_path = Path(args.input_file)
    public_key_path = Path(args.public_key)
    output_path = Path(args.output_file)
    
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    if not public_key_path.exists():
        print(f"Error: Public key file '{public_key_path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    # Read input file
    print(f"Reading input file: {input_path}")
    input_data = read_file(input_path)
    print(f"Input size: {len(input_data)} bytes")
    
    # Compress data
    print("Compressing data...")
    compressed_data = compress_data(input_data)
    print(f"Compressed size: {len(compressed_data)} bytes")
    
    # Load public key
    print(f"Loading public key: {public_key_path}")
    public_key = load_public_key(public_key_path)
    
    # Encrypt data
    print("Encrypting data...")
    encrypted_data = encrypt_data(compressed_data, public_key)
    print(f"Encrypted size: {len(encrypted_data)} bytes")
    
    # Encode to base64
    print("Encoding to base64...")
    base64_data = base64.b64encode(encrypted_data).decode('ascii')
    
    # Write output file as ASCII text
    print(f"Writing encrypted output: {output_path}")
    write_text_file(output_path, base64_data)
    
    print("Encryption complete!")


def decrypt_mode(args: argparse.Namespace) -> None:
    """Handle decryption mode."""
    # Validate input files exist
    input_path = Path(args.input_file)
    private_key_path = Path(args.private_key)
    output_path = Path(args.output_file)
    
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    if not private_key_path.exists():
        print(f"Error: Private key file '{private_key_path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    # Read encrypted file (base64 encoded)
    print(f"Reading encrypted file: {input_path}")
    base64_data = read_text_file(input_path)
    
    # Decode from base64
    print("Decoding from base64...")
    try:
        encrypted_data = base64.b64decode(base64_data.encode('ascii'))
    except binascii.Error:
        print("Error: Invalid base64 encoding in input file", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error decoding base64 data: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"Encrypted size: {len(encrypted_data)} bytes")
    
    # Load private key
    print(f"Loading private key: {private_key_path}")
    
    password = None
    if args.password:
        password = get_password("Enter private key password: ")
    
    # Try to load the private key
    try:
        private_key = load_private_key(private_key_path, password)
    except SystemExit as e:
        # If loading failed and we haven't tried with password, try again
        if not password:
            print("Private key appears to be password protected.")
            password = get_password("Enter private key password: ")
            private_key = load_private_key(private_key_path, password)
        else:
            raise
    
    # Decrypt data
    print("Decrypting data...")
    compressed_data = decrypt_data(encrypted_data, private_key)
    print(f"Compressed size: {len(compressed_data)} bytes")
    
    # Decompress data
    print("Decompressing data...")
    decompressed_data = decompress_data(compressed_data)
    print(f"Decompressed size: {len(decompressed_data)} bytes")
    
    # Write output file
    print(f"Writing decrypted output: {output_path}")
    write_file(output_path, decompressed_data)
    
    print("Decryption complete!")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate RSA keys, encrypt or decrypt files using RSA keys with compression"
    )
    
    # Create subparsers for generate-keys, encrypt and decrypt commands
    subparsers = parser.add_subparsers(dest='mode', help='Operation mode')
    
    # Generate keys subcommand
    keygen_parser = subparsers.add_parser('generate-keys', help='Generate RSA key pair')
    keygen_parser.add_argument(
        "--key-size",
        type=int,
        default=2048,
        choices=[1024, 2048, 3072, 4096],
        help="RSA key size in bits (default: 2048)"
    )
    keygen_parser.add_argument(
        "--public-key",
        type=str,
        default="public_key.pem",
        help="Path to save the public key (default: public_key.pem)"
    )
    keygen_parser.add_argument(
        "--private-key",
        type=str,
        default="private_key.pem", 
        help="Path to save the private key (default: private_key.pem)"
    )
    keygen_parser.add_argument(
        "--no-password",
        action="store_true",
        help="Generate private key without password protection"
    )
    
    # Encrypt subcommand
    encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt a file')
    encrypt_parser.add_argument(
        "--input-file", "-i",
        type=str, 
        required=True,
        help="Path to the input file to encrypt"
    )
    encrypt_parser.add_argument(
        "--public-key", "-k",
        type=str, 
        required=True,
        help="Path to the RSA public key file (PEM format)"
    )
    encrypt_parser.add_argument(
        "--output-file", "-o",
        type=str, 
        required=True,
        help="Path to the output encrypted file"
    )
    
    # Decrypt subcommand
    decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt a file')
    decrypt_parser.add_argument(
        "--input-file", "-i",
        type=str, 
        required=True,
        help="Path to the encrypted input file"
    )
    decrypt_parser.add_argument(
        "--private-key", "-k",
        type=str, 
        required=True,
        help="Path to the RSA private key file (PEM format)"
    )
    decrypt_parser.add_argument(
        "--output-file", "-o",
        type=str, 
        required=True,
        help="Path to the output decrypted file"
    )
    decrypt_parser.add_argument(
        "--password", "-p",
        action="store_true",
        help="Prompt for private key password (use if private key is password protected)"
    )
    
    args = parser.parse_args()
    
    # Check if mode was provided
    if args.mode is None:
        parser.print_help()
        sys.exit(1)
    
    # Route to appropriate function
    match args.mode:
        case 'generate-keys':
            generate_keys_mode(args)
        case 'encrypt':
            encrypt_mode(args)
        case 'decrypt':
            decrypt_mode(args)
        case _:
            parser.print_help()
            sys.exit(1)


if __name__ == '__main__':
    main()