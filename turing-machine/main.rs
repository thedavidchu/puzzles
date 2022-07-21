/// A Brain F Interpreter written in Rust
use std::io;


fn get_input() -> Option<String> {
    let buffer =String::new();
    let result = io::stdin.read_line(buffer);

    match result {
        Ok => {
            return Some(buffer);
        },
        Err => {
            return None;
        }
    }

}


fn main() -> () {
    let mut tape: [u8; 30_000] = [0; 30_000];
    let mut idx: usize = 0;
    let command = String::from("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.");
    let mut ip: usize = 0;

    loop {
        if ip == command.len() {
            break;
        }

        match c {
            '>' => {
                idx = (idx + 1) % tape.len();
            },
            '<' => {
                idx = (idx - 1) % tape.len();
            },
            '+' => {
                tape[idx].wrapping_add(1i8);
            },
            '-' => {
                tape[idx].wrapping_add(-1i8);
            },
            '[' => {
                /* TODO */
                if tape[idx] == 0u8 {

                }
            },
            ']' => {
                /* TODO */
                if tape[idx] != 0u8 {

                }
            },
            '.' => {
                print!("{}", std::str::from_utf8(tape[idx] as i8).unwrap());
            },
            ',' => {
                /* TODO */
            },
            _ => {
                continue;
            }
        }
    }
}
