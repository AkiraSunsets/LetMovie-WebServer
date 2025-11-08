// --- Ponto de Entrada Principal ---
// Este evento "DOMContentLoaded" agora verifica em qual página estamos
// e executa APENAS o código necessário para aquela página.
document.addEventListener("DOMContentLoaded", async () => {
    
    // 1. Se encontrar a "#listinha", estamos na página "listar_filmes.html"
    if (document.getElementById("listinha")) {
        await carregarFilmes();
    }

    // 2. Se encontrar o "#sucesso-container", estamos na página "sucesso.html"
    if (document.getElementById("sucesso-container")) {
        await carregarDetalhesSucesso();
    }
});


// --- Lógica da Página de Sucesso ---
async function carregarDetalhesSucesso() {
    // 1. Pegar o ID da URL
    const params = new URLSearchParams(window.location.search);
    const idFilme = params.get("id");

    const loadingDiv = document.getElementById("loading-message");
    const detalhesDiv = document.getElementById("filme-detalhes");
    const errorDiv = document.getElementById("error-message");
    // const container = document.getElementById("sucesso-container"); // Já verificado acima

    if (!idFilme) {
        loadingDiv.style.display = "none";
        errorDiv.style.display = "block";
        errorDiv.querySelector("p").textContent = "Nenhum ID de filme foi fornecido.";
        return;
    }

    try {
        // 2. Fazer o fetch na nova API /api/filme/{id}
        const resp = await fetch(`/api/filme/${idFilme}`);
        if (!resp.ok) {
            throw new Error(`HTTP error! status: ${resp.status}`);
        }
        
        const filme = await resp.json();

        // 3. Preencher o HTML com os dados do filme
        // (Usando || "N/A" para campos que podem ser nulos)
        document.getElementById("filme-poster").src = filme.poster || 'https://via.placeholder.com/150x220?text=Sem+Imagem';
        document.getElementById("filme-titulo").textContent = filme.nomeFilme || "Título não encontrado";
        document.getElementById("filme-ano").textContent = filme.ano || "N/A";
        document.getElementById("filme-duracao").textContent = filme.tempo_duracao || "N/A";
        document.getElementById("filme-generos").textContent = filme.generos || "N/A";
        document.getElementById("filme-linguagens").textContent = filme.linguagens || "N/A";
        document.getElementById("filme-diretores").textContent = filme.diretores || "N/A";
        document.getElementById("filme-produtoras").textContent = filme.produtoras || "N/A";
        document.getElementById("filme-atores").textContent = filme.atores || "N/A";

        // 4. Mover o H2 de "Sucesso" para dentro da div de detalhes
        //    Isso garante que ele apareça junto com o card.
        const h2Sucesso = loadingDiv.querySelector("h2");
        detalhesDiv.prepend(h2Sucesso); // Adiciona o H2 no início do card
        
        // 5. Esconder o "carregando" e mostrar os "detalhes"
        loadingDiv.style.display = "none";
        detalhesDiv.style.display = "block";

    } catch (err) {
        console.error("Erro ao buscar detalhes do filme:", err);
        loadingDiv.style.display = "none";
        errorDiv.style.display = "block";
    }
}


// --- Lógica da Página de Listagem ---

// --- Carregar Filmes (listagem) ---
async function carregarFilmes() {
  try {
    const resp = await fetch("/api/filmes");
    if (!resp.ok) throw new Error(`HTTP error! status: ${resp.status}`);
    const filmes = await resp.json();

    const lista = document.getElementById("listinha"); 
    if (!lista) return; // Guarda de segurança

    lista.innerHTML = ""; 

    if (!filmes || filmes.length === 0) {
      lista.innerHTML = `<article class="mensagemVazia"><p>🎬 Não há filmes cadastrados.</p></article>`;
      return;
    }

    filmes.forEach((filme) => {
      const li = document.createElement("li");
      
      // Exibe os dados do seu banco de dados populado
      li.innerHTML = `
        <div class="cardFilme">
          <img src="${filme.poster || 'https://via.placeholder.com/150x220?text=Sem+Imagem'}"
               alt="Poster do filme" class="posterFilme">
          <div class="infoFilme">
            <h3>${filme.nomeFilme}</h3>
            <p><strong>Ano:</strong> ${filme.ano || "N/A"}</p>
            <p><strong>Duração:</strong> ${filme.tempo_duracao || "N/A"} min</p>
            <p><strong>Gênero(s):</strong> ${filme.generos || "N/A"}</p>
            <p><strong>Linguagem(ns):</strong> ${filme.linguagens || "N/A"}</p>
            <p><strong>Diretor(es):</strong> ${filme.diretores || "N/A"}</p>
          </div>
          <div class="infoFilmeExtra">
             <p><strong>Atores:</strong> ${filme.atores || "N/A"}</p>
          </div>
          <div class="acoesCard">
            <button class="botaoPequeno botaoPequenoExcluir" onclick="deletarFilme(${filme.id_filme})">
              <i class="bi bi-trash-fill"></i>
            </button>
          </div>
        </div>
      `;
      lista.appendChild(li);
    });
  } catch (err) {
    console.error("Erro ao carregar filmes:", err);
  }
}

/* --- Deletar Filme --- */
async function deletarFilme(id_filme) {
  if (!confirm("Tem certeza que deseja excluir este filme? Esta ação é irreversível.")) return;

  const resposta = await fetch("/delete", { 
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `id=${id_filme}` 
  });

  const data = await resposta.json(); 

  if (resposta.ok) {
    alert(data.message); 
    carregarFilmes();
  } else {
    mostrarModal(data.message || "Erro ao deletar filme.");
  }
}


const formCadastro = document.getElementById("cadastro-input"); 

if (formCadastro) {
  formCadastro.addEventListener("submit", async (e) => {
    e.preventDefault(); 
    
    const formData = new FormData(formCadastro);
    
    const resp = await fetch("/cadastro", {
      method: "POST",
      body: new URLSearchParams(formData) // Envia os dados do form
    });
    
    const data = await resp.json(); // Espera uma resposta JSON

    if (resp.ok && data.status === "sucesso") { 
      window.location.href = `/sucesso.html?id=${data.id}`;
    } else {
      mostrarModal(data.message || "Ocorreu um erro desconhecido.");
    }
  });
}

function mostrarModal(mensagem) {
  const modalAntigo = document.querySelector(".modal");
  if (modalAntigo) modalAntigo.remove();

  const modal = document.createElement("div");
  modal.classList.add("modal"); 

  const styleId = "modal-style";
  if (!document.getElementById(styleId)) {
    const style = document.createElement("style");
    style.id = styleId;
    style.innerHTML = `
      .modal { position: fixed; top: 0; left: 0; width: 100%; height: 100%;
          background: rgba(0,0,0,0.7); display: flex; align-items: center; 
          justify-content: center; z-index: 1000; }
      .modal-conteudo { background: #111; color: white; padding: 30px; 
          border-radius: 10px; text-align: center; border: 1px solid #555;
          max-width: 400px; }
      .modal-conteudo h2 { color: #E50914; margin-bottom: 15px; }
      .modal-conteudo p { margin-bottom: 20px; }
      .modal-conteudo button { background: #E50914; color: white; border: none;
          padding: 10px 20px; border-radius: 5px; cursor: pointer;
          font-weight: bold; }
    `;
    document.head.appendChild(style);
  }

  modal.innerHTML = `
    <div class="modal-conteudo">
      <h2>❌ Erro no Cadastro</h2>
      <p>${mensagem}</p>
      <button id="fecharModal">OK</button>
    </div>
  `;
  document.body.appendChild(modal);

  document.getElementById("fecharModal").addEventListener("click", () => {
    modal.remove();
  });
}