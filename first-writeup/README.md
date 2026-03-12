
## Challenge Information

- **Challenge Name:** `The Will`
- **Category:** `Reverse Engineering`
- **Platform:** `JordanSec CTF`
- **Difficulty:** `Medium`

## 1. Description

The challenge provided a Windows executable file named **`The will.exe`**. Based on the challenge description, which suggested that the program “hides a secret in the depths,” the objective was to analyze the executable, locate any hidden data, and recover the secret contained within it.

## 2. Initial Reconnaissance

The first step was to identify the file type using the `file` command:

```bash
file "The will.exe"
```

The result showed that the file is a **PE32 executable for Microsoft Windows** and specifically a **Mono/.NET assembly**. This was an important observation because .NET executables can usually be decompiled into readable source-like code using tools such as **ILSpy** or **dnSpy**, which significantly simplifies static analysis.

## 3. Static Analysis and Resource Inspection

After confirming that the executable was a .NET assembly, the next step was to inspect its internal resources. By analyzing the embedded resources using tools such as **monodis** and **ILSpy**, an encrypted file was discovered inside the executable resources:

- **Resource name:** `The_will.Resources.f1.png.enc`
- **Offset:** `552`

This indicated that the challenge likely stored important hidden content as an encrypted embedded resource rather than exposing it directly in the program logic.

The encrypted resource was then extracted using the following command:

```bash
dd if="The will.exe" bs=1 skip=552 of=f1.png.enc
```

## 4. Reverse Engineering the Decryption Logic

The executable was then decompiled in **ILSpy** to inspect the decryption routine used by the program. Through code analysis, it was determined that the application uses **AES encryption in CBC mode** with the following key:

- **Key:** `shadowpass123456`
- **Mode:** `CBC`

Based on this information, a Python script (`sol.py`) was written to decrypt the extracted file `f1.png.enc`.

Although the decryption process completed successfully, the resulting output did not immediately produce a valid PNG image. This suggested that the decrypted file contained extra bytes or padding before the actual image data.

## 5. Fixing the Decrypted File

To verify whether the output truly contained an image, the decrypted file was inspected for the standard PNG file signature:

```text
\x89PNG
```

The decrypted file did not begin with this signature, which indicated that unnecessary leading bytes had to be removed. A short Python one-liner was used to locate the real beginning of the PNG data and write a clean file:

```bash
python3 -c "data = open('fixed_flag.png', 'rb').read(); open('real_flag.png', 'wb').write(data[data.find(b'\x89PNG'):])"
```

This step successfully removed the extra leading bytes and restored the original PNG file structure.

## 6. Recovering the Flag

After cleaning the decrypted output, the file `real_flag.png` was opened and the hidden flag was successfully revealed. This confirmed that the executable stored the challenge solution inside an encrypted resource, and that the intended solving path involved:

1. identifying the .NET nature of the binary,
2. extracting the embedded encrypted resource,
3. reversing the decryption logic,
4. fixing the resulting file format,
5. and finally reading the flag from the recovered image.

## 7. Recovered Evidence

After decrypting and cleaning the output file, the hidden flag was successfully recovered as a PNG image, shown below:

![Recovered Flag](images/image.png)

## 8. Final Result

The flag was successfully recovered from the decrypted image.

## 9. Tools Used

| Tool | Purpose |
|------|---------|
| `file` / `strings` | Initial reconnaissance and text inspection |
| `monodis` | Resource and metadata inspection in the .NET executable |
| `ILSpy` | Decompiling the .NET assembly and analyzing the program logic |
| `dd` | Extracting raw data from the executable at a specific offset |
| `Python` | Implementing AES decryption and cleaning the output file |

## 10. Key Takeaways

This challenge highlights several important reverse engineering concepts:

- In reverse engineering challenges, the flag is not always stored directly in the code; it may be hidden inside embedded resources.
- For .NET executables, static analysis is often highly effective because the code can usually be decompiled with good readability.
- File signatures (magic bytes) are extremely useful when validating decryption output and recovering corrupted or padded files.
- Even when the correct decryption key and algorithm are identified, the resulting output may still require additional cleanup before it becomes usable.

## 11. Conclusion

The challenge was solved by combining static analysis, resource extraction, and cryptographic reversal. By decompiling the .NET assembly, locating the embedded encrypted resource, recovering the AES-CBC decryption parameters, and correcting the decrypted output using the PNG magic bytes, the hidden image was successfully restored and the flag was obtained.

and hey before u go this is the sol.py i used
https://github.com/naeim179/reverse-engineering-writeups/blob/main/first-writeup/sol.py