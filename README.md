# Tugas_Proyek_Akhir

## 1. Konstruksi Sintaksis & Pola Tata Bahasa (Pattern/BNF)
  Konstruksi bahasa pemrograman yang dipilih untuk implementasi tugas akhir ini adalah struktur perulangan **For Loop**. Untuk membedakan karakteristik simulator ini dengan model perulangan standar lainnya, masukan (*source code*) yang digunakan melibatkan operasi penugasan kompleks serta operasi aritmetika perkalian pada bagian tubuh perulangan (*body loop*).

### A. Contoh Kode Sumber Input
```for ( i = 1 ; i < 5 ; i = i + 1 ) { hasil = hasil * 2 }```

### B. Pola Tata Bahasa - Backus-Naur Form (BNF)
Aturan sintaksis formal yang mendasari pembentukan token dan penataan hierarki pohon ekspresi diatur lewat rumusan tata bahasa bebas konteks berikut:
<for_stmt>    ::= "for" "(" <init> ";" <condition> ";" <step> ")" "{" <statements> "}"
<init>        ::= <identifier> "=" <value>
<condition>   ::= <identifier> <operator> <value>
<step>        ::= <identifier> "=" <identifier> "+" <value>
<statements>  ::= <identifier> "=" <identifier> "*" <value>
<identifier>  ::= a | b | c | ... | z | ID
<value>       ::= integer | digit

## 2. Penjelasan Implementasi Tahapan Kompilasi
   Program simulator yang dibangun merepresentasikan empat fase krusial arsitektur kompilator modern secara sekuensial:

### A. Analisis Leksikal (Lexer / Tokenizer)
Mesin analisis leksikal bekerja memindai karakter mentah kode sumber menggunakan pemetaan ekspresi reguler (regular expression). Pada tahap ini, karakter dipotong menjadi komponen dasar terkecil bernama Token dan dikelompokkan ke dalam kategori kelas token yang spesifik:
- KEYWORD: Mengidentifikasi kata kunci sistem pengendali loop, yakni for.

- ID (Identifier): Menampung nama variabel kontainer memori seperti i dan hasil.

- NUM (Literal Number): Mengenali nilai konstanta numerik berupa angka positif tunggal maupun jamak (1, 5, 2).

- OP (Operator): Memilah simbol operasi penugasan (=), relasional logika (<), dan aritmetika matematika (+, *).

- SYM (Symbol): Menangkap komponen tanda baca struktural seperti kurung (), kurung kurawal {}, serta tanda titik koma (;) yang bertindak sebagai pembatas krusial header statements pada konstruksi for.

### B. Analisis Sintaksis (Parsing / AST Construction)
Fase penelaahan sintaksis mengemban tanggung jawab untuk menguji keabsahan susunan token terhadap hukum tata bahasa (BNF) yang telah disepakati.
- Mekanisme Ekstraksi: Parser mencari indeks pembatas berupa simbol tanda kurung dan tanda titik koma (;) guna memecah kepala perulangan (loop header) secara presisi ke dalam 3 segmen data mandiri: komponen inisialisasi awal (init), batas kondisi evaluasi (condition), dan pembaruan nilai variabel pencacah (step).

- Penyusunan Objek AST: Apabila susunan struktur dinilai valid, representasi semantik kode tersebut dibungkus ke dalam sebuah simpul pohon sintaks abstrak (Abstract Syntax Tree) konkret melalui instansiasi kelas ForNode(Node).

### C. Analisis Semantik (Semantic Analyzer)
Analisis semantik bertugas menguji makna kontekstual operan dalam struktur program guna memastikan kevalidan logika sebelum memasuki fase instruksi perantara.
- Validasi Tabel Simbol (Symbol Table Validation): Simulator melakukan pengecekan menyeluruh terhadap seluruh token berjenis ID (variabel) yang ditemukan dalam ekspresi. Setiap variabel wajib dicocokkan eksistensinya dengan kamus Environment (symbol_table).

- Penanganan Galat Semantik: Jika kode sumber menggunakan pengenal eksternal yang belum dideklarasikan di dalam alokasi tabel memori awal program, sistem secara reaktif akan melempar interupsi kesalahan makna berupa NameError (Semantic Error: Undefined Variable), sehingga mencegah pembentukan instruksi TAC ilegal.

### D. Pembangkitan Kode Antara (Intermediate Code Generation / TAC)
Fase akhir dari simulator ini memetakan objek pohon hierarki AST menjadi rangkaian instruksi linear tiga alamat atau Three-Address Code (TAC) yang ramah terhadap arsitektur perangkat keras komputer. Karena pola dasar for bersifat perulangan kondisional bertingkat, TAC dikonstruksikan menggunakan struktur lompatan berbasis GOTO logis dengan rancangan label pelompat unik:
- Eksekusi Awal (Initialization Line): Baris penugasan awal (i = 1) dijalankan tepat satu kali di bagian luar, sebelum blok pemeriksaan loop aktif.

- Label Evaluasi (FOR_CHECK): Berfungsi sebagai pos pemeriksaan berulang. Apabila condition terpenuhi (bernilai true), aliran eksekusi diarahkan melompat masuk menuju label tubuh instruksi (GOTO FOR_BODY). Jika gagal (false), alur kode langsung dialihkan keluar menuju penanda akhir (GOTO FOR_EXIT).

- Label Eksekusi (FOR_BODY): Mengeksekusi rangkaian operasi inti di dalam perulangan (hasil = hasil * 2).

- Mekanisme Inkrementasi Otomatis: Baris operasi pembaruan nilai pencacah (i = i + 1) disisipkan secara otomatis oleh pembangkit TAC di baris terbawah blok FOR_BODY. Instruksi ditutup dengan perintah mutlak GOTO FOR_CHECK untuk memaksa program melompat kembali ke atas demi menguji ulang kondisi variabel.

## 3. Hasil Pengujian
```=== INPUT SOURCE CODE (FOR LOOP) ===
for ( i = 1 ; i < 5 ; i = i + 1 ) { hasil = hasil * 2 }

--- TAHAP 1: ANALISIS LEKSIKAL (Tokenisasi For) ---
Token: for        | Tipe: KEYWORD
Token: (          | Tipe: SYM
Token: i          | Tipe: ID
Token: =          | Tipe: OP
Token: 1          | Tipe: NUM
Token: ;          | Tipe: SYM
Token: i          | Tipe: ID
Token: <          | Tipe: OP
Token: 5          | Tipe: NUM
Token: ;          | Tipe: SYM
Token: i          | Tipe: ID
Token: =          | Tipe: OP
Token: i          | Tipe: ID
Token: +          | Tipe: OP
Token: 1          | Tipe: NUM
Token: )          | Tipe: SYM
Token: {          | Tipe: SYM
Token: hasil      | Tipe: ID
Token: =          | Tipe: OP
Token: hasil      | Tipe: ID
Token: *          | Tipe: OP
Token: 2          | Tipe: NUM
Token: }          | Tipe: SYM

--- TAHAP 2 & 3: ANALISIS SINTAKSIS & SEMANTIK (AST) ---
➔ Objek AST Berhasil Dibuat: ForNode
➔ AST Sub-Tree Init        : i = 1
➔ AST Sub-Tree Kondisi     : i < 5
➔ AST Sub-Tree Step        : i = i + 1
➔ AST Sub-Tree Body        : hasil = hasil * 2

--- TAHAP 4: GENERASI TAC FOR LOOP ---
// --- Inisialisasi awal ---
i = 1

FOR_CHECK_1:
if i < 5 GOTO FOR_BODY_1
GOTO FOR_EXIT_1

FOR_BODY_1:
  hasil = hasil * 2
  i = i + 1 // Pembaruan nilai loop
GOTO FOR_CHECK_1

FOR_EXIT_1:```
