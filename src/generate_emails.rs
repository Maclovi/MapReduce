use rand::{Rng, distr::Alphanumeric};
use std::fs::File;
use std::io::{BufWriter, Write};
use std::path::Path;

const TARGET_SIZE: u64 = 2 * 1024_u64.pow(3); // 2 GiB
const CHUNK_SIZE: usize = 65 * 1024; // 65 KiB

fn random_email(length: usize) -> String {
    let domains = ["@ya.ru", "@yohoo.com", "@gmai.com", "@mail.ru"];
    let name: String = rand::rng()
        .sample_iter(&Alphanumeric)
        .take(length)
        .map(char::from)
        .collect();
    let domain = domains[rand::rng().random_range(0..domains.len())];
    format!("{}{}\n", name.to_lowercase(), domain)
}

pub fn run() -> std::io::Result<()> {
    let path = Path::new("emails.txt");
    let file = File::create(path)?;
    let mut writer = BufWriter::new(file);

    let mut current_size: u64 = 0;

    while current_size < TARGET_SIZE {
        let mut buffer = String::with_capacity(CHUNK_SIZE);

        // Примерно 20 байт на email
        let count = CHUNK_SIZE / 20;

        for _ in 0..count {
            buffer.push_str(&random_email(10));
        }

        writer.write_all(buffer.as_bytes())?;
        current_size += buffer.len() as u64;
    }

    writer.flush()?;
    Ok(())
}
