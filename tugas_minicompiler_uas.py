import re

class Node:
    pass

class ForNode(Node):
    def __init__(self, init, condition, step, body):
        self.init = init           # Bagian awal
        self.condition = condition # Kondisi batas
        self.step = step           # Pembaruan nilai
        self.body = body           # Pernyataan di dalam loop

class ForCompilerUnik:
    def __init__(self, source_code, symbol_table=None):
        self.source = source_code
        self.symbol_table = symbol_table if symbol_table is not None else {}
        self.label_idx = 1

    # --- FASE 1: ANALISIS LEKSIKAL (Lexer) ---
    def lexical_analysis(self):
        token_patterns = [
            ('KEYWORD', r'\bfor\b'),
            ('ID', r'\b[a-zA-Z_]\w*\b'),
            ('NUM', r'\b\d+\b'),
            ('OP', r'[><=!]+|[+\-*/=]'),
            ('SYM', r'[(){};]'), # Menambahkan titik koma ';' sebagai simbol pemisah for loop
        ]
        
        master_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns)
        tokens_list = []
        
        for match in re.finditer(master_pattern, self.source):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            tokens_list.append({'type': token_type, 'value': token_value})
            
        return tokens_list

    # --- FASE 2 & 3: ANALISIS SINTAKSIS & SEMANTIK (Parser & AST) ---
    def syntax_and_semantic_parse(self, tokens):
        raw_values = [t['value'] for t in tokens]
        
        # Validasi struktur utama
        if not raw_values or raw_values[0] != 'for':
            raise SyntaxError("Sintaks Error: Kode harus diawali kata kunci 'for'.")
        if '(' not in raw_values or ')' not in raw_values or '{' not in raw_values or '}' not in raw_values:
            raise SyntaxError("Sintaks Error: Tanda kurung tidak lengkap.")
            
        try:
            open_p = raw_values.index('(')
            close_p = raw_values.index(')')
            open_b = raw_values.index('{')
            close_b = raw_values.index('}')
            
            # Memotong isi di dalam ( ) berdasarkan tanda titik koma ';'
            header_tokens = raw_values[open_p + 1 : close_p]
            header_str = "".join(header_tokens)
            parts = header_str.split(';')
            
            if len(parts) != 3:
                raise SyntaxError("Sintaks Error: Struktur di dalam 'for(...)' harus memiliki 2 tanda titik koma ';'.")
                
            init_str = parts[0].strip()
            condition_str = parts[1].strip()
            step_str = parts[2].strip()
            body_str = " ".join(raw_values[open_b + 1 : close_b]).strip()
            
            # Analisis Semantik: Validasi Variabel ke Symbol Table
            for tok in tokens:
                if tok['type'] == 'ID' and tok['value'] != 'for':
                    if tok['value'] not in self.symbol_table:
                        raise NameError(f"Semantik Error: Variabel '{tok['value']}' tidak terdaftar di Symbol Table.")
                        
            return ForNode(init_str, condition_str, step_str, body_str)
            
        except ValueError:
            raise SyntaxError("Sintaks Error: Penempatan kurung pembuka/penutup salah.")

    # --- FASE 4: INTERMEDIATE CODE GENERATION (TAC) ---
    def generate_three_address_code(self):
        tokens = self.lexical_analysis()
        ast_root = self.syntax_and_semantic_parse(tokens)
        
        lbl_start = f"FOR_CHECK_{self.label_idx}"
        lbl_body = f"FOR_BODY_{self.label_idx}"
        lbl_exit = f"FOR_EXIT_{self.label_idx}"
        self.label_idx += 1
        
        # Struktur TAC untuk FOR:
        tac_instructions = [
            f"// --- Inisialisasi awal ---",
            f"{ast_root.init}",
            f"",
            f"{lbl_start}:",
            f"if {ast_root.condition} GOTO {lbl_body}",
            f"GOTO {lbl_exit}",
            f"",
            f"{lbl_body}:",
            f"  {ast_root.body}",
            f"  {ast_root.step} // Pembaruan nilai loop",
            f"GOTO {lbl_start}",
            f"",
            f"{lbl_exit}:"
        ]
        return tac_instructions


# --- UJI COBA INPUT BARU ---
if __name__ == "__main__":
    lbl_identitas = "ADE_FOR"
    
    # Memori variabel (Symbol Table)
    # Kita daftarkan variabel 'i' untuk counter dan 'hasil' untuk kalkulasi didalamnya
    memori_variabel = {'i': 0, 'hasil': 1}
    
    # INPUT BARU: Struktur FOR dengan perkalian di dalam body-nya
    kode_mentah = "for ( i = 1 ; i < 5 ; i = i + 1 ) { hasil = hasil * 2 }"
    
    print(f"=== INPUT SOURCE CODE (FOR LOOP) ===\n{kode_mentah}\n")
    
    try:
        compiler = ForCompilerUnik(kode_mentah, memori_variabel)
        
        print("--- TAHAP 1: ANALISIS LEKSIKAL (Tokenisasi For) ---")
        daftar_token = compiler.lexical_analysis()
        for token in daftar_token:
            print(f"Token: {token['value']:<10} | Tipe: {token['type']}")
            
        print("\n--- TAHAP 2 & 3: ANALISIS SINTAKSIS & SEMANTIK (AST) ---")
        pohon_ast = compiler.syntax_and_semantic_parse(daftar_token)
        print(f"➔ Objek AST Berhasil Dibuat: {type(pohon_ast).__name__}")
        print(f"➔ AST Sub-Tree Init        : {pohon_ast.init}")
        print(f"➔ AST Sub-Tree Kondisi     : {pohon_ast.condition}")
        print(f"➔ AST Sub-Tree Step        : {pohon_ast.step}")
        print(f"➔ AST Sub-Tree Body        : {pohon_ast.body}")
        
        print("\n--- TAHAP 4: GENERASI TAC FOR LOOP ---")
        hasil_tac = compiler.generate_three_address_code()
        for baris in hasil_tac:
            print(baris)
            
    except Exception as e:
        print(f"Kompilasi Gagal! Alasan: {e}")