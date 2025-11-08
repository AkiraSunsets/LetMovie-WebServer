import os
import re
import json
import mysql.connector
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

# --- Conexão com o Banco de Dados ---
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",       # <-- VERIFIQUE SUA SENHA
        database="LetMovie"
    )
    print("✅ Conexão com o banco de dados 'LetMovie' estabelecida.")
except mysql.connector.Error as err:
    print(f"❌ Erro ao conectar ao MySQL: {err}")
    exit(1)

# --- Classe Principal do Servidor ---
class MyHandle(SimpleHTTPRequestHandler):

    # Função auxiliar para parsing de nomes
    def parse_name(self, full_name):
        parts = full_name.strip().split(' ', 1)
        nome = parts[0]
        sobrenome = parts[1] if len(parts) > 1 else ''
        return nome, sobrenome

    # Função auxiliar para buscar ou criar IDs
    def get_or_create_id(self, cursor, table_name, name_str, extra_cols=None):
        nome, sobrenome = self.parse_name(name_str)
        
        if table_name == 'Produtora':
            sql_find = "SELECT ID FROM Produtora WHERE Nome = %s"
            cursor.execute(sql_find, (name_str,))
        elif sobrenome:
            sql_find = f"SELECT ID FROM {table_name} WHERE Nome = %s AND Sobrenome = %s"
            cursor.execute(sql_find, (nome, sobrenome))
        else:
            sql_find = f"SELECT ID FROM {table_name} WHERE Nome = %s"
            cursor.execute(sql_find, (nome,))
            
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            if table_name == 'Ator' or table_name == 'Diretor':
                sql_insert = f"INSERT INTO {table_name} (Nome, Sobrenome, id_nacionalidade, id_generopessoa) VALUES (%s, %s, NULL, NULL)"
                cursor.execute(sql_insert, (nome, sobrenome))
            else: # Produtora
                sql_insert = f"INSERT INTO {table_name} (Nome) VALUES (%s)"
                cursor.execute(sql_insert, (name_str,))
                
            return cursor.lastrowid
    
    # --- Métodos GET ---
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path # Limpa os parâmetros (ex: ?id=23)

        # Rota API: /api/filmes
        if path == "/api/filmes":
            try:
                if not mydb.is_connected(): mydb.reconnect()
                cursor = mydb.cursor(dictionary=True)
                
                sql = """
                    SELECT 
                        f.ID AS id_filme, f.Titulo AS nomeFilme, f.TempoDuracao AS tempo_duracao,
                        f.Ano AS ano, f.Poster AS poster,
                        GROUP_CONCAT(DISTINCT g.Nome SEPARATOR ', ') AS generos,
                        GROUP_CONCAT(DISTINCT CONCAT(a.Nome, ' ', a.Sobrenome) SEPARATOR ', ') AS atores,
                        GROUP_CONCAT(DISTINCT CONCAT(d.Nome, ' ', d.Sobrenome) SEPARATOR ', ') AS diretores,
                        GROUP_CONCAT(DISTINCT l.Nome SEPARATOR ', ') AS linguagens
                    FROM Filme f
                    LEFT JOIN GeneroFilme gf ON f.ID = gf.id_filme
                    LEFT JOIN Genero g ON gf.id_genero = g.ID
                    LEFT JOIN AtorFilme af ON f.ID = af.id_filme
                    LEFT JOIN Ator a ON af.id_ator = a.ID
                    LEFT JOIN FilmeDiretor fd ON f.ID = fd.id_filme
                    LEFT JOIN Diretor d ON fd.id_diretor = d.ID
                    LEFT JOIN LinguagemFilme lf ON f.ID = lf.id_filme
                    LEFT JOIN Linguagem l ON lf.id_linguagem = l.ID
                    GROUP BY f.ID ORDER BY f.Titulo;
                """
                cursor.execute(sql)
                filmes = cursor.fetchall()
                cursor.close()

                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-t")
                self.end_headers()
                self.wfile.write(json.dumps(filmes, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_error(500, f"Erro ao buscar filmes: {str(e)}")

        # Rota API: /api/filme/{id}
        elif re.match(r"/api/filme/(\d+)", path):
            try:
                filme_id = path.split("/")[-1]
                if not mydb.is_connected(): mydb.reconnect()
                cursor = mydb.cursor(dictionary=True)
                
                sql = """
                    SELECT 
                        f.ID AS id_filme, f.Titulo AS nomeFilme, f.TempoDuracao AS tempo_duracao,
                        f.Ano AS ano, f.Poster AS poster,
                        GROUP_CONCAT(DISTINCT g.Nome SEPARATOR ', ') AS generos,
                        GROUP_CONCAT(DISTINCT CONCAT(a.Nome, ' ', a.Sobrenome) SEPARATOR ', ') AS atores,
                        GROUP_CONCAT(DISTINCT CONCAT(d.Nome, ' ', d.Sobrenome) SEPARATOR ', ') AS diretores,
                        GROUP_CONCAT(DISTINCT l.Nome SEPARATOR ', ') AS linguagens,
                        GROUP_CONCAT(DISTINCT p.Nome SEPARATOR ', ') AS produtoras
                    FROM Filme f
                    LEFT JOIN GeneroFilme gf ON f.ID = gf.id_filme
                    LEFT JOIN Genero g ON gf.id_genero = g.ID
                    LEFT JOIN AtorFilme af ON f.ID = af.id_filme
                    LEFT JOIN Ator a ON af.id_ator = a.ID
                    LEFT JOIN FilmeDiretor fd ON f.ID = fd.id_filme
                    LEFT JOIN Diretor d ON fd.id_diretor = d.ID
                    LEFT JOIN LinguagemFilme lf ON f.ID = lf.id_filme
                    LEFT JOIN Linguagem l ON lf.id_linguagem = l.ID
                    LEFT JOIN ProdutoraFilme pf ON f.ID = pf.id_filme
                    LEFT JOIN Produtora p ON pf.id_produtora = p.ID
                    WHERE f.ID = %s
                    GROUP BY f.ID;
                """
                cursor.execute(sql, (filme_id,))
                filme = cursor.fetchone()
                cursor.close()

                if filme:
                    self.send_response(200)
                    self.send_header("Content-type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps(filme, ensure_ascii=False).encode("utf-8"))
                else:
                    self.send_error(404, "Filme não encontrado")
            except Exception as e:
                self.send_error(500, f"Erro ao buscar filme: {str(e)}")

        # =================================================================
        # CORREÇÃO 2: Adicionada rota para /sucesso.html
        # =================================================================
        elif path == "/sucesso.html":
            # self.path ainda contém "?id=23", mas o super() vai procurar
            # o arquivo /html/sucesso.html, que é o correto.
            self.path = "/html/sucesso.html"
            return super().do_GET()

        # Servir arquivos estáticos (CSS, JS, HTML)
        else:
            if path == "/":
                self.path = "/html/index.html"
            elif path == "/sucesso.js":
                 self.path = "/js/script.js"

            try:
                return super().do_GET()
            except IOError:
                self.send_error(404, f"Arquivo não encontrado: {self.path}")


    # --- Métodos POST ---
    def do_POST(self):
        path = urlparse(self.path).path
        
        # Função interna para enviar resposta JSON
        def send_json_response(status_code, content):
            self.send_response(status_code)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(content, ensure_ascii=False).encode('utf-8'))

        # Rota POST: /cadastro
        if path in ["/cadastro", "/cadastro/"]:
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            data = {
                'titulo': form_data.get('nome', [''])[0].strip(),
                'atores': form_data.get('atores', [''])[0].strip(),
                'diretor': form_data.get('diretor', [''])[0].strip(),
                'ano': form_data.get('ano', [''])[0].strip(),
                'duracao': form_data.get('duracao', [''])[0].strip() or None,
                'id_genero': form_data.get('id_genero', [''])[0].strip(),
                'produtora': form_data.get('produtora', [''])[0].strip(),
                'id_linguagem': form_data.get('id_linguagem', [''])[0].strip(),
                'poster': form_data.get('urlposter', [''])[0].strip() or None,
            }

            try:
                if not all([data['titulo'], data['atores'], data['diretor'], data['ano'], 
                            data['duracao'], data['id_genero'], data['produtora'], 
                            data['id_linguagem'], data['poster']]):
                    raise ValueError("Todos os campos são obrigatórios.")
                
                if not data['ano'].isdigit() or not (1900 <= int(data['ano']) <= 2099):
                    raise ValueError("Ano inválido. Deve ser um número entre 1900 e 2099.")
                
                if not data['duracao'].isdigit() or int(data['duracao']) <= 0:
                    raise ValueError("Duração inválida. Deve ser um número positivo.")
                int(data['id_genero'])
                int(data['id_linguagem'])
            except ValueError as ve:
                send_json_response(400, {"status": "erro", "message": str(ve)})
                return
            except Exception:
                send_json_response(400, {"status": "erro", "message": "Dados inválidos."})
                return

            try:
                if not mydb.is_connected(): mydb.reconnect()
                cursor = mydb.cursor()
                
                # =================================================================
                # CORREÇÃO 1: Removida a linha mydb.start_transaction()
                # =================================================================
                
                cursor.execute("SELECT ID FROM Filme WHERE Titulo = %s", (data['titulo'],))
                if cursor.fetchone():
                    raise mysql.connector.Error(errno=1062, msg="Já existe um filme com esse título!")

                sql_filme = "INSERT INTO Filme (Titulo, TempoDuracao, Ano, Poster) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_filme, (data['titulo'], int(data['duracao']), int(data['ano']), data['poster']))
                id_filme = cursor.lastrowid

                cursor.execute("INSERT INTO GeneroFilme (id_genero, id_filme) VALUES (%s, %s)", (int(data['id_genero']), id_filme))
                cursor.execute("INSERT INTO LinguagemFilme (id_linguagem, id_filme) VALUES (%s, %s)", (int(data['id_linguagem']), id_filme))

                id_produtora = self.get_or_create_id(cursor, 'Produtora', data['produtora'])
                cursor.execute("INSERT INTO ProdutoraFilme (id_filme, id_produtora) VALUES (%s, %s)", (id_filme, id_produtora))
                
                id_diretor = self.get_or_create_id(cursor, 'Diretor', data['diretor'])
                cursor.execute("INSERT INTO FilmeDiretor (id_filme, id_diretor) VALUES (%s, %s)", (id_filme, id_diretor))

                atores_list = [ator.strip() for ator in data['atores'].split(',')]
                for ator_nome in atores_list:
                    if ator_nome:
                        id_ator = self.get_or_create_id(cursor, 'Ator', ator_nome)
                        cursor.execute("INSERT INTO AtorFilme (id_filme, id_ator) VALUES (%s, %s)", (id_filme, id_ator))

                mydb.commit() # A transação implícita é finalizada aqui
                cursor.close()
                send_json_response(200, {"status": "sucesso", "id": id_filme})

            except mysql.connector.Error as err:
                mydb.rollback() # A transação implícita é revertida aqui
                if err.errno == 1062:
                    send_json_response(409, {"status": "erro", "message": "Já existe um filme com esse título!"})
                else:
                    send_json_response(500, {"status": "erro", "message": f"Erro de banco de dados: {err.msg}"})
            except Exception as e:
                mydb.rollback()
                send_json_response(500, {"status": "erro", "message": f"Erro interno do servidor: {str(e)}"})

        # Rota POST: /delete
        elif self.path == '/delete':
            filme_id_str = None
            try:
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length).decode('utf-8')
                form_data = parse_qs(body)

                filme_id_str = form_data.get('id', [None])[0]
                if not filme_id_str or not filme_id_str.isdigit():
                    send_json_response(400, {"status": "erro", "message": "ID do filme inválido ou não fornecido."})
                    return
                
                filme_id = int(filme_id_str)

                if not mydb.is_connected(): mydb.reconnect()
                cursor = mydb.cursor()
                
                # =================================================================
                # CORREÇÃO 1: Removida a linha mydb.start_transaction()
                # =================================================================

                print(f"--- Iniciando exclusão do Filme ID: {filme_id} ---")

                # Deleta de TODAS as tabelas de junção primeiro
                print(f"Deletando de AtorFilme...")
                cursor.execute("DELETE FROM AtorFilme WHERE id_filme = %s", (filme_id,))
                
                print(f"Deletando de GeneroFilme...")
                cursor.execute("DELETE FROM GeneroFilme WHERE id_filme = %s", (filme_id,))
                
                print(f"Deletando de FilmeDiretor...")
                cursor.execute("DELETE FROM FilmeDiretor WHERE id_filme = %s", (filme_id,))
                
                print(f"Deletando de LinguagemFilme...")
                cursor.execute("DELETE FROM LinguagemFilme WHERE id_filme = %s", (filme_id,))
                
                print(f"Deletando de ProdutoraFilme...")
                cursor.execute("DELETE FROM ProdutoraFilme WHERE id_filme = %s", (filme_id,))
                
                print(f"Deletando de PaisFilme...")
                cursor.execute("DELETE FROM PaisFilme WHERE id_filme = %s", (filme_id,))
                
                # Agora, deleta o filme principal
                print(f"Deletando da tabela principal Filme...")
                cursor.execute("DELETE FROM Filme WHERE ID = %s", (filme_id,))
                
                if cursor.rowcount == 0:
                    print(f"Erro: Filme ID {filme_id} não encontrado na tabela Filme.")
                    mydb.rollback() 
                    send_json_response(404, {"status": "erro", "message": "Filme não encontrado."})
                    return

                # Sucesso!
                mydb.commit() # A transação implícita é finalizada aqui
                cursor.close()
                print(f"--- Sucesso! Filme ID: {filme_id} deletado. ---")
                send_json_response(200, {"status": "sucesso", "message": "Filme deletado com sucesso."})

            except mysql.connector.Error as err:
                mydb.rollback() # A transação implícita é revertida aqui
                print(f"\n❌ ERRO DE BANCO DE DADOS AO DELETAR ID {filme_id_str}: {err}\n")
                send_json_response(500, {"status": "erro", "message": f"Erro de banco de dados: {err.msg}"})
            
            except Exception as e:
                mydb.rollback()
                print(f"\n❌ ERRO INTERNO DO SERVIDOR AO DELETAR ID {filme_id_str}: {e}\n")
                send_json_response(500, {"status": "erro", "message": f"Erro interno do servidor: {str(e)}"})
        
        else:
            super(MyHandle, self).do_POST()

def main():
    # Muda o diretório de execução para a pasta raiz (WEB-SERVER)
    initial_dir = os.getcwd()
    if os.path.basename(initial_dir) == 'server':
        new_dir = os.path.join(initial_dir, '..')
        print(f"Executando de dentro da pasta /server. Mudando diretório para: {os.path.abspath(new_dir)}")
        os.chdir(new_dir)
    
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print(f"🚀 Servidor rodando em http://localhost:8000")
    print(f"Servindo arquivos do diretório: {os.getcwd()}")
    httpd.serve_forever()

if __name__ == '__main__':
    main()