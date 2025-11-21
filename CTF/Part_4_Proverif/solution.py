from pwn import *
import re

HOST = 'svtctf.m0lecon.it'
PORT = 13448
context.log_level = 'error'  # Suppress connection info for cleaner output

def solve():

    # We open both connections to get the public keys (B1, B2) needed for the swap.
    # We do NOT send data to s2 yet, keeping its timer paused (State: Fresh).
    s1 = remote(HOST, PORT)
    s1.recvuntil(b"key: ")
    B1 = int(s1.recvline())

    s2 = remote(HOST, PORT)
    s2.recvuntil(b"key: ")
    B2 = int(s2.recvline())

    # We send s2's key to s1 to force the shared secret creation.
    # Then we wait for "Response?" to confirm s1 has timed out and output the Challenge.
    s1.sendlineafter(b"key:", str(B2).encode())
    s1.recvuntil(b"challenge: ")
    
    # Simple parsing: read the hex line directly
    challenge = s1.recvline().strip().decode()
    print(f"[*] Challenge: {challenge}")

    # NOW we activate s2. It is fresh (Responder mode). We send s1's key, then the challenge.
    # s2 will compute the correct response for us.
    s2.sendlineafter(b"key:", str(B1).encode())
    s2.sendlineafter(b"(hex):", challenge.encode())

    # We grab all hex strings from s2's output. The one that isn't the challenge is our response.
    response_data = s2.recvall(timeout=2).decode(errors='ignore')
    candidates = re.findall(r'[0-9a-f]{64}', response_data)
    response = next(c for c in candidates if c != challenge)
    
    print(f"[*] Response:  {response}")

    # Authenticate s1 with the oracle's response to get the flag.
    s1.sendline(response.encode())
    print(f"\n[+] FLAG: {s1.recvall().strip().decode()}\n")

if __name__ == "__main__":
    solve()