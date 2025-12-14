#!/usr/bin/env python3
import re
ref = 'Galatians 5.22-6.2'
# Normalize dots to colons
ref = ref.replace('.', ':')
print(f"Normalized: {ref}")
match = re.match(r'^([A-Za-z0-9 ]+)\s+(\d+):(.+)$', ref.strip())
print(f"Match: {match}")
if match:
    book, chapter, verses = match.groups()
    print(f"Book: {book}, Chapter: {chapter}, Verses: {verses}")
