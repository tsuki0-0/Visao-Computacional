## 👁️ Inteligência de Visão Corporativa

> Uma plataforma de visão computacional de ponta projetada para segmentação de instâncias em tempo real, impulsionada pelo YOLOv8, desenvolvida com Streamlit e integrada de forma fluida ao PostgreSQL nativo da nuvem (Neon.tech).

## 💡 A Ideia Principal (Pt-br)
- Em aplicações modernas de visão computacional, unir a inferência de modelos de IA com a persistência de dados estruturados é um grande desafio de engenharia. O Enterprise Vision Intelligence foi desenvolvido para resolver exatamente esse gargalo.

- O objetivo principal deste repositório é fornecer um projeto leve e pronto para produção que recebe um input visual não estruturado (upload de imagem).
- Executa segmentação de instâncias baseada em deep learning, extrai metadados estruturais e semânticos granulares, e grava instantaneamente esses insights em um banco de dados relacional na nuvem.
- Tudo integrado a uma interface web reativa e moderna, sem exigir infraestrutura pesada de GPU local.

## 🏗️ Arquitetura e Como Funciona
- O sistema opera através de um pipeline automatizado de 4 estágios:

Plaintext:
```

[ Upload do Usuário ] ──> [ Camada Streamlit UI ] ──> [ Ultralytics YOLOv8-seg ] 
                                                                  │
                                                                  ▼
[ Neon.tech PostgreSQL ] <── [ Metadados Estruturados ] <── [ Extração OpenCV / NumPy ]
Ingestão e Interface (Streamlit):
O usuário envia uma imagem através de um componente web seguro. O frontend gerencia o estado da aplicação de forma limpa, garantindo que as variáveis de metadados sejam inicializadas dinamicamente.
```

- ## Inferência de IA e Segmentação (Ultralytics YOLO):
- A aplicação carrega o modelo yolov8n-seg.pt (em cache para otimização de performance), processa a matriz da imagem, plota as máscaras de segmentação e caixas delimitadoras, e identifica as classes dos objetos.

- ## Extração de Características (Pillow / NumPy):
- Simultaneamente, atributos estruturais (largura e altura em pixels, formato, modo) e métricas quantitativas (total de instâncias, classes únicas) são compilados em um relatório analítico.

- ## Persistência em Nuvem (Neon.tech / PostgreSQL):
- Por meio de uma conexão transacional com psycopg2, o sistema cria automaticamente a tabela de logs (image_analysis_logs) caso ela não exista, executando inserções SQL parametrizadas diretamente na nuvem.

## 🌟 Principais Recursos
- Comparação Visual em Painel Duplo: Inspecione instantaneamente a imagem original lado a lado com a saída segmentada pelo YOLO.

- Métricas Dinâmicas de Metadados: Cálculo automatizado de resolução, formato de arquivo, contagem de instâncias e distribuições categóricas.

- Integração Nativa com Banco de Dados na Nuvem: Configuração flexível através de injeção dinâmica de variáveis de ambiente para o Neon.tech.

- Desempenho Otimizado para CPU: Conjunto de dependências cuidadosamente ajustado permitindo o deploy sem atritos em servidores de nuvem (como o Render).

## 👁️ Enterprise Vision Intelligence

> A cutting-edge computer vision platform designed for real-time instance segmentation powered by YOLOv8, built with Streamlit, and seamlessly integrated with cloud-native PostgreSQL (Neon.tech).

--- 

## 💡 The Core Concept (EN-US)

- In modern computer vision applications, bridging the gap between raw AI model inference and structured data persistence is a major engineering challenge. **Enterprise Vision Intelligence** was built to solve this exact bottleneck. 

- The main objective of this repository is to provide a lightweight, production-ready blueprint that takes an unstructured visual input (an image upload), executes deep learning-based instance segmentation, extracts granular structural and semantic metadata, and instantly commits those insights into a cloud relational database—all wrapped inside a modern, reactive web interface without requiring heavy local GPU infrastructure.

---

## 🏗️ Architecture & How It Works

- The system operates on an automated 4-stage processing pipeline:

```
[ User Upload ] ──> [ Streamlit UI Layer ] ──> [ Ultralytics YOLOv8-seg ] 
                                                          │
                                                          ▼
[ Neon.tech PostgreSQL ] <── [ Structured Metadata ] <── [ OpenCV / NumPy Extraction ]
Ingestion & UI Layer (Streamlit):

- The user supplies an image through a secure web component. The frontend handles state management cleanly, ensuring metadata variables (dimensions, format, filename) are initialized dynamically upon upload.

```

- ## AI Inference & Instance Segmentation (Ultralytics YOLO):
- The application loads the yolov8n-seg.pt model (cached via memory for performance optimization). It processes the image matrix, plots instance segmentation boundaries, masks, and bounding boxes, and extracts detected object classes.

- ## Feature Extraction (Pillow / NumPy):
- Simultaneously, structural attributes (exact pixel width, height, format, mode) and quantitative metrics (total instances, unique classes) are compiled into a structured analytical report.

- ## Cloud Persistence (Neon.tech / PostgreSQL):
- Via a transactional connection using psycopg2, the system automatically provisions the target table (image_analysis_logs) if it doesn't exist, securely executing parameterized SQL insertions to log every analytical session directly to the cloud.

## 🌟 Key Features

- Dual-Pane Visual Comparison: Instantly inspect the raw input image side-by-side with the YOLO-segmented output.

- Dynamic Metadata Metrics: Automated calculation of resolution, file format, instance counts, and categorical distributions.

- Cloud-Native Database Integration: Zero-configuration local friction with dynamic runtime environment variable injection for Neon.tech.

- CPU-Optimized Performance: Carefully tuned dependency stack allowing seamless deployment on server environments like Render without requiring high-end GPUs.
