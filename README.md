# MapReduce Email Processor

## First of all

Ensure you have either **Python 3.10+** or **Rust (with Cargo)** installed.

This project processes large files of email addresses using parallel map-reduce-style aggregation.

---

## Generate emails.txt

You can generate a ~2 GB file of random emails with:

### Option 1: Python

```bash
python src/generate_emails.py
```

### Option 2: Rust

```bash
cargo run --release
```

## Run MapReduce

### With Python (async + process pool):

```bash
python src/mapreduce.py
```

Make sure emails.txt is present in the current directory.
