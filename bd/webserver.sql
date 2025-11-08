CREATE DATABASE LetMovie;
USE LetMovie;

CREATE TABLE Filme (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    Titulo VARCHAR(255) NOT NULL,
    TempoDuracao INT,
    Ano INT NOT NULL,
    Poster TEXT
);

CREATE TABLE Nacionalidade (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL
);

CREATE TABLE GeneroPessoa (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    Titulo VARCHAR(255) NOT NULL
);

CREATE TABLE Ator (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL,
    Sobrenome VARCHAR(255) NOT NULL,
	id_nacionalidade INT,
    id_generopessoa INT,
    FOREIGN KEY (id_nacionalidade) REFERENCES Nacionalidade(ID),
    FOREIGN KEY (id_generopessoa) REFERENCES GeneroPessoa(ID)
);

CREATE TABLE AtorFilme (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    id_filme INT NOT NULL,
    id_ator INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES Filme(ID),
    FOREIGN KEY (id_ator) REFERENCES Ator(ID)
);

CREATE TABLE Genero (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL
);

CREATE TABLE GeneroFilme (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    id_genero INT NOT NULL,
    id_filme INT NOT NULL,
    FOREIGN KEY (id_genero) REFERENCES Genero(ID),
    FOREIGN KEY (id_filme) REFERENCES Filme(ID)
);

CREATE TABLE Diretor (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL,
    Sobrenome VARCHAR(255) NOT NULL,
	id_nacionalidade INT,
    id_generopessoa INT,
    FOREIGN KEY (id_nacionalidade) REFERENCES Nacionalidade(ID),
    FOREIGN KEY (id_generopessoa) REFERENCES GeneroPessoa(ID)
);

CREATE TABLE FilmeDiretor (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    id_filme INT NOT NULL,
    id_diretor INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES Filme(ID),
    FOREIGN KEY (id_diretor) REFERENCES Diretor(ID)
);

CREATE TABLE Linguagem (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL
);

CREATE TABLE LinguagemFilme (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    id_filme INT NOT NULL,
    id_linguagem INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES Filme(ID),
    FOREIGN KEY (id_linguagem) REFERENCES Linguagem(ID)
);

CREATE TABLE Produtora (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL
);

CREATE TABLE ProdutoraFilme (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    id_filme INT NOT NULL,
    id_produtora INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES Filme(ID),
    FOREIGN KEY (id_produtora) REFERENCES Produtora(ID)
);

CREATE TABLE Pais (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR(255) NOT NULL
);

CREATE TABLE PaisFilme (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    id_pais INT NOT NULL,
    id_filme INT NOT NULL, 
    FOREIGN KEY (id_pais) REFERENCES Pais(ID),
    FOREIGN KEY (id_filme) REFERENCES Filme(ID)
);

-- Inserts corrigidos
INSERT INTO Filme (Titulo, TempoDuracao, Ano, Poster)
VALUES 
("Como eu era antes de você", 110, 2012, "https://m.media-amazon.com/images/M/MV5BMjQ4ZGMyZjYtNDYwNC00MmUyLWE4ZWQtM2ViMTQ0OTc1M2U1XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg"),
("A culpa é das estrelas", 126, 2014, "https://upload.wikimedia.org/wikipedia/pt/0/08/The_Fault_in_Our_Stars_%28filme%29.jpg"),
("P.S. Eu Te Amo", 126, 2007, "https://upload.wikimedia.org/wikipedia/pt/thumb/4/42/P_s_i_love_you.jpg/250px-P_s_i_love_you.jpg"),
("Um Dia", 107, 2011, "https://upload.wikimedia.org/wikipedia/pt/a/ad/One_Day_Poster.jpg"),
("Querido John", 108, 2010, "https://br.web.img2.acsta.net/medias/nmedia/18/87/32/42/20028691.jpg"),
("Estrada da Furia", 120, 2015, "https://upload.wikimedia.org/wikipedia/pt/thumb/2/23/Max_Mad_Fury_Road_Newest_Poster.jpg/250px-Max_Mad_Fury_Road_Newest_Poster.jpg"),
("A chegada", 116, 2016, "https://cinemacao.com/wp-content/uploads/2016/11/arrival-tsrposter-brazil.jpg"),
("Corra!", 104, 2017, "https://br.web.img3.acsta.net/pictures/17/04/19/21/08/577190.jpg"),
("O lobo de Wall Street", 180, 2013, "https://upload.wikimedia.org/wikipedia/pt/thumb/8/8d/The_Wolf_of_Wall_Street.jpg/250px-The_Wolf_of_Wall_Street.jpg"),
("O rei Leão", 88, 1994, "https://m.media-amazon.com/images/I/91VjLtvtPkL._UF894,1000_QL80_.jpg"),
("Parasita", 132, 2019, "https://br.web.img2.acsta.net/pictures/19/10/04/19/58/1046648.jpg"),
("La La Land", 128, 2016, "https://upload.wikimedia.org/wikipedia/pt/thumb/c/c0/La_La_Land_%28filme%29.png/250px-La_La_Land_%28filme%29.png"),
("Gladiador", 155, 2000, "https://upload.wikimedia.org/wikipedia/pt/4/44/GladiadorPoster.jpg"),
("Toy Story 3", 103, 2010, "https://m.media-amazon.com/images/I/911ytdKwucL.jpg"),
("A origem", 148, 2010, "https://upload.wikimedia.org/wikipedia/pt/8/84/AOrigemPoster.jpg"),
("O Grande Hotel", 99, 2014, "https://br.web.img3.acsta.net/medias/nmedia/18/95/49/34/20408653.jpg"),
("O sexto sentido", 107, 1999, "https://br.web.img2.acsta.net/medias/nmedia/18/90/53/94/20101506.jpg"),
("Homem-Aranha no aranhaverso", 117, 2018, "https://www.sonypictures.com.br/sites/brazil/files/2023-06/1400x2100.jpg"),
("O Fabuloso Destino de Amélie", 122, 2001, "https://upload.wikimedia.org/wikipedia/pt/a/a0/Le_fabuleux_destin_d%27Am%C3%A9lie_Poulain.jpg"),
("O Senhor dos Anéis - A sociedade do anel", 178, 2001, "https://br.web.img3.acsta.net/medias/nmedia/18/92/91/32/20224832.jpg"),
("Clube de Luta", 139, 1999, "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSNAklmRu_o2m6mcmMXzTiVSOFAt3gmUDdy8Hd5pr6SDnujHz7kls4BT3dFHy9OvOkxV8BHAaGWage5w1t-NxBb02nl_Vdteo5OZsACmA"),
("Divertida Mente", 95, 2015, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcShPeyKUi0XDjg4qFq2NkJx4Fj_TxmHpNPxog&s");

INSERT INTO Nacionalidade (Nome)
VALUES 
("Americana"),
("Britânica"),
("Canadense"),
("Francesa"),
("Alemã"),
("Australiana"),
("Neozelandesa"),
("Espanhola"),
("Italiana"),
("Portuguesa"),
("Sul-Coreana"),
("Japonesa"),
("Chinesa"),
("Indiana"),
("Mexicana"),
("Argentina"),
("Sueca"),
("Norueguesa"),
("Irlandesa"),
("Russa"),
("Dinamarquesa"),
("Sueca");

INSERT INTO GeneroPessoa (Titulo)
VALUES
("Feminino"),
("Masculino");

INSERT INTO Ator (Nome, Sobrenome, id_nacionalidade,id_generopessoa)
VALUES
("Emilia", "Clarke", 2, 1),
("Shailene", "Woodley", 1, 1),
("Hilary", "Swank", 1, 1),
("Anne", "Hathaway", 1, 1),
("Channing", "Tatum", 2, 2),
("Tom", "Hardy", 2, 2),
("Amy", "Adams", 1, 1),
("Daniel", "Kaluuya", 2, 2),
("Leonardo", "DiCaprio", 1, 2),
("James", "Earl Jones", 1, 2),
("Song", "Kang-ho", 11, 2),
("Ryan", "Gosling", 3, 2),
("Russell", "Crowe", 7, 2),
("Tom", "Hanks", 1, 2),
("Cillian", "Murph", 19, 2),
("Ralph", "Fiennes", 2, 2),
("Bruce", "Willis", 1, 2),
("Shameik", "Moore", 1, 2),
("Audrey", "Tautou", 4, 1),
("Elijah", "Wood", 1, 2),
("Brad", "Pitt", 1, 2),
("Amy", "Poehler", 1, 1);

INSERT INTO AtorFilme (id_filme, id_ator)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13),
(14, 14),
(15, 15),
(16, 16),
(17, 17),
(18, 18),
(19, 19),
(20, 20),
(21, 21),
(22, 22);

INSERT INTO Genero (Nome)
VALUES
("Romance"),
("Drama"),
("Ação"),
("Ficção Científica"),
("Aventura"),
("Terror"),
("Mistério"),
("Suspense"),
("Biografia"),
("Comédia"),
("Crime"),
("Animação"),
("Musical"),
("Fantasia"),
("Documentário"),
("Comédia Romantica"),
("Policial"),
("Guerra"),
("Noir"),
("Histórico");

INSERT INTO GeneroFilme (id_genero, id_filme)
VALUES
(1,1),
(2,2),
(1,3),
(1,4),
(1,5),
(3, 6),
(4, 7),
(6, 8),
(9, 9),
(12, 10),
(2, 11),
(13, 12),
(3, 13),
(12, 14),
(3, 15),
(10, 16),
(2, 17),
(12, 18),
(10, 19),
(5, 20),
(2, 21),
(10, 22);

INSERT INTO Diretor (Nome, Sobrenome, id_nacionalidade, id_generopessoa)
VALUES
("Thea", "Sharrock", 2, 1),
("Josh", "Boone", 1, 2),
("Richard", "LaGravenese", 1, 2),
("Lone", "Scherfig", 21, 1),
("Lasse", "Hallström", 22, 2),
("George", "Miller", 6, 2),
("Denis", "Villeneuve", 3, 2),
("Jordan", "Peele", 1, 2),
("Martin", "Scorsese", 1, 2),
("Roger", "Allers", 1, 2),
("Bong", "Joon-ho", 11, 2),
("Damien", "Chazelle", 1, 2),
("Ridley", "Scott", 2, 2),
("Lee", "Unkrich", 1, 2),
("Christopher", "Nolan", 2, 2),
("Wes", "Anderson", 1, 2),
("M.", "Night Shyamalan", 1, 2),
("Bob", "Persichetti", 1, 2),
("Jean-Pierre", "Jeunet", 4, 2),
("Peter", "Jackson", 7, 2),
("David", "Fincher", 1, 2),
("Peter", "Docter", 1, 2);

INSERT INTO FilmeDiretor (id_filme, id_diretor)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13),
(14, 14),
(15, 15),
(16, 16),
(17, 17),
(18, 18),
(19, 19),
(20, 20),
(21, 21),
(22, 22);

INSERT INTO Linguagem (Nome)
VALUES
('Português'),
('Inglês'),
('Espanhol'),
('Francês'),
('Alemão'),
('Italiano'),
('Japonês'),
('Chinês'),
('Coreano'),
('Russo'),
('Árabe'),
('Hindi'),
('Grego'),
('Turco'),
('Holandês'),
('Polonês'),
('Sueco'),
('Norueguês'),
('Hebraico'),
('Tailandês');

INSERT INTO LinguagemFilme (id_linguagem, id_filme)
VALUES
(2, 1),
(2, 2),
(2, 3),
(2, 4),
(2, 5),
(2, 6),
(2, 7),
(2, 8),
(2, 9),
(2, 10),
(9, 11),
(2, 12),
(2, 13),
(2, 14),
(2, 15),
(2, 16),
(2, 17),
(2, 18),
(2, 19),
(2, 20),
(2, 21),
(2, 22);

INSERT INTO Produtora (Nome)
VALUES
("New Line Cinema"),
("20th Century Fox"),
("Warner Bros. Pictures"),
("Focus Features"),
("Relativity Media"),
("RatPac-Dune Entertainment"),
("21 Laps Entertainment"),
("Blumhouse Productions"),
("Red Granite Pictures"),
("Walt Dinsey Feature Animation"),
("Barunson E&A"),
("Summit Entertainment"),
("DreamWorks SKG"),
("Pixar Animation Studios"),
("Syncopy"),
("Indian Paintbrush"),
("Hollywood Pictures"),
("Sony Pictures Animation"),
("Claudie Ossard Productions"),
("WingNut Films"),
("Regency Enterprises");

INSERT INTO ProdutoraFilme (id_filme, id_produtora)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13),
(14, 14),
(15, 15),
(16, 16),
(17, 17),
(18, 18),
(19, 19),
(20, 20),
(21, 21),
(22, 14);

INSERT INTO Pais (Nome)
VALUES
("Reino Unido"),
("Estados Unidos"),
("Austrália"),
("Canadá"),
("Coreia do Sul"),
("Nova Zelândia"),
("França"),
("Brasil");

INSERT INTO PaisFilme(id_pais, id_filme)
VALUES
(2, 1),
(2, 2),
(2, 3),
(1, 4),
(2, 5),
(3, 6),
(2, 7),
(2, 8),
(2, 9),
(2, 10),
(5, 11),
(2, 12),
(1, 13),
(2, 14),
(2, 15),
(2, 16),
(2, 17),
(2, 18),
(7, 19),
(6, 20),
(2, 21),
(2, 22);
