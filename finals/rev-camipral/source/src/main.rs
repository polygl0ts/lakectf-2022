use std::env;
use std::io;

fn main() {
    println!(
        "Welcome to Camipral, the EPFL fortune teller.\nWhat is your 6 digits camipro number?"
    );

    let mut camipro_string = String::new();
    io::stdin()
        .read_line(&mut camipro_string)
        .expect("failed to read camipro");

    let camipro_parse = camipro_string.trim().parse::<u32>();

    if camipro_string.len() != 7 || camipro_parse.is_err() {
        println!("Camipral only accepts valid camipro numbers\n");
        return;
    }

    let camipro = camipro_parse.unwrap();

    println!("Student {camipro}, what is your lucky number?");

    let mut lucky_number_string = String::new();
    io::stdin()
        .read_line(&mut lucky_number_string)
        .expect("failed to read lucky number");

    let lucky_number = lucky_number_string
        .trim()
        .parse::<u32>()
        .unwrap_or_default();

    let lucky_result = camipro.saturating_mul((camipro % 42) + lucky_number);

    if lucky_result < camipro {
        let flag = env::var("FLAG").unwrap_or_else(|_| "EPFL{this_is_not_a_flag}".to_string());
        println!("This is your lucky day!");
        println!("{flag}");
    } else {
        println!("Camipral does not predict much luck in your future");
    }
}
