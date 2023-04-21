import pandas as pd  #python3 -m pip install pandas
import plotly_express as px #python3 -m pip install plotly-express
import streamlit as st
from streamlit_option_menu import option_menu

#--- 
st.set_page_config(page_title="Böter 22/23", 
                    page_icon="📊", #:Money-Mouth Face:
                    layout='wide') 

#Read Data From Excel Sheets
@st.cache_data
def get_df_from_Excel():
    df = pd.read_excel(
        io='Fine-Test-New.xlsx',
        engine='openpyxl',
        sheet_name='Ny_Master_Data',
        skiprows=1,
        usecols='A:F',
        nrows=876,
    )
    return df

df = get_df_from_Excel()

@st.cache_data
def get_leaderboard_df():
    df_leaderboard = pd.read_excel(
        io='Fine-Test-New.xlsx',
        engine='openpyxl',
        sheet_name='Top_stats',
        skiprows=0,
        usecols='A:G',
        nrows=28,
    )
    return df_leaderboard
df_leaderBoard = get_leaderboard_df()

# --- Functions ---
def getOccurenceOfFine (dataframe, fine :str, fine_amount : int):
    occurrence = int(dataframe.loc[dataframe["Bot"]==fine].sum().get("Böter")/fine_amount) 
    return occurrence

def getFineCatAmountPerMonth (category:str): 
    finesForCat = df_selection.loc[df_selection["Kategori"]==category].groupby(by="Månad").sum().sort_values(by="Månad")
    return finesForCat

#Title & Navigation
st.markdown("<h2 style='text-align: center;'> Böter Säsong 22/23 📊", unsafe_allow_html=True)

selected_page = option_menu(
    menu_title= "Välj en Dashboard-nivå",
    options =["Lag Nivå", "Indvid(er) Nivå"],
    icons=["cash-coin", "person-circle"],
    orientation = "horizontal"
)

# --------------------------------- TEAM Level Dashboard ----------------------------------------
if selected_page == "Lag Nivå":
    st.sidebar.header("Filtrer på Lagnivå")
    
    # TEAM Filters
    position = st.sidebar.multiselect(
    "Välj Positioner: ",
    options=df["Position"].unique(),
    default=df["Position"].unique(),
    help="Välj vilka Positioner som ska inkldueras"
    )
    
    fine_type = st.sidebar.multiselect(
    "Välj böteskategori: ",
    options=df["Kategori"].unique(),
    default=df["Kategori"].unique(),
    help="Välj vilka böteskategorier som ska inkluderas"   
    )

    df_selection = df.query(
    "Position == @position & Kategori == @fine_type"
    )

    # TEAM: Main KPIs
    col_1, col_2,col_3 = st.columns(3)
    with col_1:
        total_fines = int(df_selection["Böter"].sum())
        st.subheader("Total :moneybag:")
        st.subheader(str(total_fines) + " kr")
    
    with col_2:
        average_fines_player =  int(df_selection.groupby(by=["Spelare"]).sum().mean())
        st.subheader("Snitt á spelare :man-playing-handball:")
        st.subheader(str(average_fines_player) + " kr")

    with col_3:
        average_fines_month =  int(df_selection.groupby(by=["Månad"]).sum().mean())
        st.subheader("Snitt á månad :calendar:")
        st.subheader(str(average_fines_month) + " kr")

    st.markdown('##')
    st.markdown("---")

    # TEAM: Monthly payments bar chart
    st.markdown("<h3 style='text-align: center;'> Böter per månad 📅", unsafe_allow_html=True)
    left_col,mid_col,right_col = st.columns([1,6,1])

    with left_col:
        st.write("")

    with mid_col:
        fines_by_month = (
            df_selection.groupby(by=["Månad"]).sum()[["Böter"]].sort_values(by="Böter")
        )

        fig_bar_monthly = px.bar(
            fines_by_month,
            x = fines_by_month.index,
            y= "Böter",
            orientation= "v",
            template="plotly_white",
            text="Böter",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_bar_monthly.update_layout(
            plot_bgcolor= "rgba(0,0,0,0)",
            yaxis = (dict(showgrid=False))
            
        )
        st.plotly_chart(fig_bar_monthly, use_container_width=True)
    
    with right_col:
        st.write("")
    st.markdown("---")

    # TEAM:Positions pie chart
    st.markdown("<h3 style='text-align: center;'> Böter per position 🤾‍♂️", unsafe_allow_html=True)
    left_col,mid_col,right_col = st.columns([1,6,1])

    with left_col:
        st.write("")

    with mid_col:
        fig_pie_position = px.pie(
            df_selection,
            names="Position",
            values ="Böter",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_pie_position.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie_position)

    with right_col:
        st.write("")
    st.markdown("---")

    #TEAM: Leader board
    st.markdown("<h3 style='text-align: center;'>Leaderboard Top 3 📊", unsafe_allow_html=True)
    st.markdown('##')

    col_1, col_2, col_3 = st.columns(3)
    with col_1: 
        st.subheader("Årets Kassakor 🤑")
        st.dataframe(df_leaderBoard.get(["Spelare","Total"]).head(3))
        st.subheader("Årets Sparsamma 🐷")
        st.dataframe(df_leaderBoard.get(["Spelare","Total"]).sort_values(by="Total").head(3))
    
    with col_2:
        st.subheader("Årets Bredbenta ⛩")
        st.dataframe(df_leaderBoard.get(["Spelare","Tunnlar"]).sort_values(by="Tunnlar", ascending=False).head(3))
        st.subheader("Årets Tak 🏘")
        st.dataframe(df_leaderBoard.get(["Spelare", "Tak"]).sort_values(by="Tak", ascending=False).head(3))
        
    with col_3:
        st.subheader("Årets Klantiga 😵‍💫")
        st.dataframe(df_leaderBoard.get(["Spelare","Skötsel"]).sort_values(by="Skötsel", ascending=False).head(3))
        st.subheader("Årets Bossar 👴")
        st.dataframe(df_leaderBoard.get(["Spelare","Bosse"]).sort_values(by="Bosse", ascending=False).head(3))
    st.markdown('##')

    # TEAM: Fines per category 
    # Fines types
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Fotboll ⚽", unsafe_allow_html=True)
    st.markdown('##')

    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        st.subheader("Tunnlar ⛩")
        st.subheader(str(getOccurenceOfFine(df_selection, "Tunnel", 10)) + " st")
        
    with col_2:
        st.subheader("Tak 🏘")
        st.subheader(str(getOccurenceOfFine(df_selection,"Tak", 30)) + " st")


    with col_3: 
        st.subheader("Rad läktare 📶")
        st.subheader(str(getOccurenceOfFine(df_selection, "Rad läktare", 10)) + " st")

    with col_4:
        st.subheader("Spelförstörelse ❌")
        st.subheader(str(getOccurenceOfFine(df_selection, "Spelförstörelse", 50)) + " st")
    st.markdown('##')

    # Handball Fines 
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Handboll Träning🤾‍♂️", unsafe_allow_html=True)
    st.markdown('##')

    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        st.subheader("Lim 🍯")
        st.subheader(str(getOccurenceOfFine(df_selection, "Lim", 100)) + " st")
        
    with col_2:
        st.subheader("Bosse 👴")
        st.subheader(str(getOccurenceOfFine(df_selection, "Bosse", 50)) + " st")


    with col_3: 
        st.subheader("Headshots 😵")
        st.subheader(str(getOccurenceOfFine(df_selection, "Skott i huvet", 100)) + " st")

    with col_4:
        st.subheader("Mål #2️⃣9️⃣")
        st.subheader(str(getOccurenceOfFine(df_selection, "29de målet", 50)) + " st")
    st.markdown('##')

    # Manners
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Skötsel 😵‍💫", unsafe_allow_html=True)
    st.markdown('##')
    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        st.subheader("Förseningsminuter ⏰")
        st.subheader(str(getOccurenceOfFine(df_selection,"Försening träning", 15))+ " min (Träning)")
        st.subheader(str(getOccurenceOfFine(df_selection,"Försening match/video", 30)) + " min (Match/Video)")

    with col_2:
        st.subheader("Bolltvättar 🏐🧹")
        st.subheader(str(getOccurenceOfFine(df_selection, "Missad bolltvätt", 50)) + " st")
         
    with col_3: 
        st.subheader("Missad Dusch 🚿")
        st.subheader(str(getOccurenceOfFine(df_selection,"Dusch", 50)) + " st")
    
    with col_4:
        st.subheader("Svineri 🐷")
        st.subheader(str(getOccurenceOfFine(df_selection,"Svineri", 50))+ " st")
        st.subheader(str(getOccurenceOfFine(df_selection,"Grovt svineri", 150))+ " st (Grova)")

    # Fun/Party
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Skoj/Fest 💃 🪩 🕺", unsafe_allow_html=True)
    st.markdown('##')
    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        st.subheader("Bilder 📸")
        st.subheader(str(getOccurenceOfFine(df_selection, "Bild i tidning", 10)) + " st") 
        
    with col_2:
        st.subheader("Första Sidor 📰")
        st.subheader(str(getOccurenceOfFine(df_selection, "Bild i tidnign (första sida)", 50)) + " st")  
        
    with col_3: 
        st.subheader("Dum bot 😵‍💫")
        st.subheader(str(getOccurenceOfFine(df_selection,"Dum-bot", 50)) + " st")

    with col_4:
        st.subheader("Casanova 👩‍❤️‍💋‍👨")
        st.subheader(str(getOccurenceOfFine(df_selection,"Hångel på klubb", 50)) + " st (Sven)")

# ---------------------------------------------------------------------------------------------------
# -------------------------------- Indivudual Level Dashboard ---------------------------------------
if selected_page == "Indvid(er) Nivå":
    st.sidebar.header("Filter på individnivå")

    player = st.sidebar.multiselect(
        "Välj Spelare: ",
        options=df["Spelare"].unique(),
        default="Affe",
        help="Välj vilken/vilka spelare som ska inkluderas"
    )

    df_individual = df.query(
        "Spelare == @player"
    )

    # ME: Main KPIs
    col_1, col_2,col_3 = st.columns(3)
    with col_1:
        total_fines = int(df_individual["Böter"].sum())
        st.subheader("Total :moneybag:")
        st.subheader(str(total_fines) + " kr")
    
    with col_2:
        average_fines_player =  int(df_individual.groupby(by=["Spelare"]).sum().mean())
        st.subheader("Snitt á spelare :man-playing-handball:")
        st.subheader(str(average_fines_player) + " kr")

    with col_3:
        average_fines_month =  int(df_individual.groupby(by=["Månad"]).sum().mean())
        st.subheader("Snitt á månad :calendar:")
        st.subheader(str(average_fines_month) + " kr")

    st.markdown('##')
    st.markdown("---")

    
    # ME: Fines per month
    st.markdown("<h3 style='text-align: center;'> Böter per månad 📅", unsafe_allow_html=True)
    left_col,mid_col,right_col = st.columns([1,6,1])

    with left_col:
        st.write("")

    with mid_col:
        fines_by_month = (
            df_individual.groupby(by=["Månad"]).sum()[["Böter"]].sort_values(by="Böter")
        )

        fig_bar_monthly = px.bar(
            fines_by_month,
            x = fines_by_month.index,
            y= "Böter",
            orientation= "v",
            template="plotly_white",
            text="Böter",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_bar_monthly.update_layout(
            plot_bgcolor= "rgba(0,0,0,0)",
            yaxis = (dict(showgrid=False))
            
        )
        st.plotly_chart(fig_bar_monthly, use_container_width=True)
    
    with right_col:
        st.write("")
    st.markdown("---")

    # --- ME: Fine Category --- 
    st.markdown("<h3 style='text-align: center;'>Böter per kategori 🔣", unsafe_allow_html=True)
    left_col, right_col = st.columns(2)

    #Fine by category bar chart
    with left_col: 
        fines_by_category= (
            df_individual.groupby(by=["Kategori"]).sum()[["Böter"]].sort_values(by="Böter")
        )

        fig_bar_category = px.bar(
            fines_by_category,
            x=fines_by_category.index,
            y="Böter", 
            orientation="v",
            template="plotly_white",
            color_discrete_sequence=px.colors.sequential.RdBu
            )

        st.plotly_chart(fig_bar_category, use_container_width=True)

    #Fines by category pie chart
    with right_col:
        fig_pie_category = px.pie(
            df_individual,
            names="Kategori",
            values ="Böter",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig_pie_category)
    # ------

    # ME: Fines types KPIs
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Fotboll ⚽", unsafe_allow_html=True)
    st.markdown('##')

    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        st.subheader("Tunnlar ⛩")
        st.subheader(str(getOccurenceOfFine(df_individual, "Tunnel", 10)) + " st")
        
    with col_2:
        st.subheader("Tak 🏘")
        st.subheader(str(getOccurenceOfFine(df_individual,"Tak", 30)) + " st")

    with col_3: 
        st.subheader("Rad läktare 📶")
        st.subheader(str(getOccurenceOfFine(df_individual,"Rad läktare", 10)) + " st")

    with col_4:
        st.subheader("Spelförstörelse ❌")
        st.subheader(str(getOccurenceOfFine(df_individual,"Spelförstörelse", 50)) + " st")
    st.markdown('##')

    # Handball Fines 
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Handboll Träning🤾‍♂️", unsafe_allow_html=True)
    st.markdown('##')

    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        st.subheader("Lim 🍯")
        st.subheader(str(getOccurenceOfFine(df_individual, "Lim", 100)) + " st")
        
    with col_2:
        st.subheader("Bosse 👴")
        st.subheader(str(getOccurenceOfFine(df_individual, "Bosse", 50)) + " st")


    with col_3: 
        st.subheader("Headshots 😵")
        st.subheader(str(getOccurenceOfFine(df_individual, "Skott i huvet", 100)) + " st")

    with col_4:
        st.subheader("Mål #2️⃣9️⃣")
        st.subheader(str(getOccurenceOfFine(df_individual,"29de målet", 50)) + " st")
    st.markdown('##')

    # Manners
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Skötsel 😵‍💫", unsafe_allow_html=True)
    st.markdown('##')
    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        st.subheader("Förseningsminuter ⏰")
        st.subheader(str(getOccurenceOfFine(df_individual,"Försening träning", 15))+ " min (Träning)")
        st.subheader(str(getOccurenceOfFine(df_individual,"Försening match/video", 30)) + " min (Match/Video)")
    
    with col_2:
        st.subheader("Bolltvättar 🏐🧹")
        st.subheader(str(getOccurenceOfFine(df_individual,"Missad bolltvätt", 50))+ " st")
         
    with col_3: 
        st.subheader("Missad Dusch 🚿")
        st.subheader(str(getOccurenceOfFine(df_individual, "Dusch", 50)))

    with col_4:
        st.subheader("Svineri 🐷")
        st.subheader(str(getOccurenceOfFine(df_individual, "Svineri", 50)) + " st")
        st.subheader(str(getOccurenceOfFine(df_individual,"Grovt svineri", 150))+ " st (Grova)")


    # Fun/Party
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Skoj/Fest 💃 🪩 🕺", unsafe_allow_html=True)
    st.markdown('##')
    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        st.subheader("Bilder 📸")
        st.subheader(str(getOccurenceOfFine(df_individual, "Bild i tidning", 10)) + " st") 
        
    with col_2:
        st.subheader("Första Sidor 📰")
        st.subheader(str(getOccurenceOfFine(df_individual,"Bild i tidnign (första sida)", 50)) + " st")  
        
    with col_3: 
        st.subheader("Dum bot 😵‍💫")
        st.subheader(str(getOccurenceOfFine(df_individual, "Dum-bot", 50)) + " st")

    with col_4:
        st.subheader("Huvudbonad 🤠 ")
        st.subheader(str(getOccurenceOfFine(df_individual,"Huvudbonadsmåndag", 50)+ getOccurenceOfFine(df_individual, "Huvudbonad vid möte/måltid",50)) + " st")
