# Bibliotecas Importadas
import os
from PIL import Image
import numpy as np
import streamlit as st
import psycopg2
from ultralytics import YOLO

# Configuração corporativa da página Streamlit
st.set_page_config(
    page_title="Enterprise Vision Intelligence | YOLO & Neon.tech",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS customizada para padrão profissional
st.markdown("""
    <style>
        .main-header { font-size: 28px; font-weight: 700; color: #1E3A8A; margin-bottom: 0px; }
        .sub-header { font-size: 16px; color: #4B5563; margin-bottom: 20px; }
        .stButton>button { width: 100%; background-color: #2563EB; color: white; font-weight: 600; border-radius: 6px; }
        .stButton>button:hover { background-color: #1D4ED8; color: white; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">Enterprise Vision Intelligence</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Plataforma Avançada de Segmentação de Imagens com YOLO e PostgreSQL (Neon.tech)</p>', unsafe_allow_html=True)

# Gerenciamento de Conexão com o Banco de Dados PostgreSQL (Neon.tech)
def get_db_connection():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        return None
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS image_analysis_logs (
                        id SERIAL PRIMARY KEY,
                        filename VARCHAR(255),
                        width INT,
                        height INT,
                        format VARCHAR(50),
                        detected_objects TEXT,
                        total_instances INT,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()
            conn.close()
        except Exception:
            pass

init_db()

# Barra lateral para parâmetros de infraestrutura
with st.sidebar:
    st.header("⚙️ Configurações")
    db_url_input = st.text_input("DATABASE_URL (Neon.tech)", type="password", help="Insira a string de conexão fornecida pelo Neon.tech.")
    if db_url_input:
        os.environ["DATABASE_URL"] = db_url_input
        # Inicializa a tabela dinamicamente caso a URL seja inserida via barra lateral
        init_db()
    
    st.markdown("---")
    st.markdown("**Modelo Ativo:** `YOLOv8n-seg`")
    st.markdown("**Framework:** Ultralytics / Streamlit")

# Carregamento otimizado do modelo YOLO com cache
@st.cache_resource
def load_yolo_model():
    return YOLO("yolov8n-seg.pt")

with st.spinner("Inicializando pesos do modelo YOLO..."):
    model = load_yolo_model()

# Componente de Upload
uploaded_file = st.file_uploader("Selecione um arquivo de imagem para processamento analítico", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Extração de metadados definida no escopo correto
    width, height = image.size
    img_format = image.format or "Desconhecido"
    filename = uploaded_file.name
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown("### 📥 Imagem de Entrada")
        st.image(image, use_container_width=True)

    # Execução da Inferência de Segmentação
    with st.spinner("Executando pipeline de segmentação..."):
        results = model(image)
        res_plotted = results[0].plot() # Renderização das máscaras e caixas delimitadoras
        
        detected_classes = []
        if results[0].boxes is not None:
            for box in results[0].boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                detected_classes.append(class_name)

    with col2:
        st.markdown("### 📤 Saída Segmentada (YOLO)")
        st.image(res_plotted, channels="BGR", use_container_width=True)

    st.markdown("---")
    
    # Ações e Persistência
    col_action, col_spacer = st.columns([1, 2])
    with col_action:
        persist_button = st.button("💾 Persistir Dados no Neon.tech")

    if persist_button:
        unique_objects = ", ".join(set(detected_classes)) if detected_classes else "Nenhum objeto identificado"
        total_instances = len(detected_classes)
        description = f"Segmentação concluída. Classes detectadas: {unique_objects}. Instâncias totais: {total_instances}."

        conn = get_db_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO image_analysis_logs (filename, width, height, format, detected_objects, total_instances, description)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (filename, width, height, img_format, unique_objects, total_instances, description))
                    conn.commit()
                conn.close()
                st.success("Transação concluída com sucesso: Dados gravados na nuvem (Neon.tech).")
            except Exception as e:
                st.error(f"Falha na operação de banco de dados: {e}")
        else:
            st.warning("Aviso: Variável de ambiente `DATABASE_URL` não configurada corretamente na barra lateral.")

    # Painel Analítico de Resultados (agora com as variáveis garantidas)
    st.markdown("### 📊 Relatório Técnico de Metadados")
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    metrics_col1.metric("Resolução", f"{width}x{height} px")
    metrics_col2.metric("Formato", img_format)
    metrics_col3.metric("Total de Instâncias", len(detected_classes))
    metrics_col4.metric("Classes Únicas", len(set(detected_classes)))

    st.json({
        "arquivo": filename,
        "dimensoes": {"largura": width, "altura": height},
        "formato_arquivo": img_format,
        "classes_detectadas": detected_classes
    })
