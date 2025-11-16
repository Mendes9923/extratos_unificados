import streamlit as st
import pandas as pd
import io



st.set_page_config(page_title="Unificador de Extratos", layout="centered")

# 🏢 Carregar e exibir a logo no topo
st.image("61805fd0-7390-471e-a9f9-e92292097cdc.webp", width=250)

st.title("📑 Unificador de Extratos Bancários")
st.write("Faça upload de múltiplos arquivos Excel para consolidar em um único arquivo.")

# 🔽 Lista de bancos (adicione conforme sua necessidade)
bancos = [
    "Banco do Brasil",
    "Bradesco",
    "Caixa Econômica",
    "Itaú",
    "Santander",
    "Sicoob",
    "Outros"
]

# 🏦 Escolher nome do banco ou nome manual
banco_escolhido = st.selectbox("Selecione o banco:", bancos)

# 📝 Definir nome personalizado para o arquivo (opcional)
nome_arquivo = st.text_input(
    "Digite o nome para o arquivo final (sem .xlsx)", 
    value=f"Extratos_{banco_escolhido.replace(' ', '_')}"
)

# ⬆️ Upload dos arquivos
uploaded_files = st.file_uploader(
    "Escolha os arquivos Excel", 
    type=["xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    dataframes = []

    for uploaded_file in uploaded_files:
        try:
            df = pd.read_excel(uploaded_file)

            # Nome da conta a partir do nome do arquivo (sem extensão)
            nome_conta = uploaded_file.name.replace(".xlsx", "")

            df["Conta"] = nome_conta  # Adiciona coluna da conta

            dataframes.append(df)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo {uploaded_file.name}: {e}")

    # 🔗 Unindo todos os DataFrames
    df_final = pd.concat(dataframes, ignore_index=True)

    st.success("Arquivos combinados com sucesso!")

    st.dataframe(df_final)

    # 💾 Gerar arquivo Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_final.to_excel(writer, index=False, sheet_name='Consolidado')

    # 🔽 Botão de download com nome personalizado
    st.download_button(
        label="📥 Baixar Excel Consolidado",
        data=output.getvalue(),
        file_name=f"{nome_arquivo}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
# 🔽 Rodapé fixo com créditos
st.markdown(
    """
    <hr style="margin-top:50px">
    <div style='text-align: center; color: grey;'>
        Desenvolvido por <strong>Daniel Mendes</strong>
    </div>
    """,
    unsafe_allow_html=True
)