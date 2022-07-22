/// A Brain F Interpreter written in Rust

fn print_instruction(instructions: &String, ip: &usize) {
    println!("{}", instructions.chars().nth(*ip).unwrap());
}

fn print_char(c: &u8) {
    match *c {
        9..=13 => print!("{}", *c as char),
        0..=31 => print!("_"),
        32..=126 => print!("{}", *c as char),
        127..=u8::MAX => print!("_"),
    }
}

fn get_next(instructions: &String, ip: &usize) -> Option<usize> {
    let mut tmp: usize = *ip;
    while tmp < instructions.len() {
        if instructions.chars().nth(tmp).unwrap() == ']' {
            return Some(tmp);
        }
        tmp += 1;
    }

    return None;
}

fn get_prev(instructions: &String, ip: &usize) -> Option<usize> {
    let mut tmp: usize = *ip;
    loop {
        if instructions.chars().nth(tmp).unwrap() == '[' {
            return Some(tmp);
        }

        if tmp == 0 {
            return None;
        }
        tmp -= 1;
    }
}

fn main() -> () {
    let mut data: [u8; 100] = [0; 100];
    let mut dp: usize = 0;
    // let instructions = String::from("++++++++>++++>++>+<-<-<-");
    // let instructions = String::from("++++++++++++++++++++++++++++++++++++++.");
    // let instructions = String::from("++[->+<]");
    // let instructions = String::from("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.");
    let instructions: String = String::from(">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.[-]>++++++++[<++++>-]<.>+++++++++++[<+++++>-]<.>++++++++[<+++>-]<.+++.------.--------.[-]>++++++++[<++++>-]<+.[-]++++++++++.");
    let mut ip: usize = 0;

    loop {
        if ip >= instructions.len() {
            break;
        }
        match instructions.chars().nth(ip).unwrap() {
            '>' => {
                dp = dp + 1;
            }
            '<' => {
                dp = dp - 1;
            }
            '+' => data[dp] = data[dp].wrapping_add(1u8),
            '-' => data[dp] = data[dp].wrapping_add(u8::MAX),
            '[' => {
                if data[dp] == 0u8 {
                    ip = match get_next(&instructions, &ip) {
                        Some(tmp_ip) => tmp_ip,
                        None => instructions.len(),
                    };
                }
            }
            ']' => {
                if data[dp] != 0u8 {
                    ip = match get_prev(&instructions, &ip) {
                        Some(tmp_ip) => tmp_ip,
                        None => instructions.len(),
                    };
                }
            }
            '.' => print_char(&data[dp]),
            ',' => { /* TODO */ }
            _ => {}
        }
        ip += 1;
    }
}
