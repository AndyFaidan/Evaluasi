import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Penelitian",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Menampilkan judul aplikasi di tengah
st.markdown("""
    <h2 style="text-align: center;">📊Layanan Mahasiswa</h2>
""", unsafe_allow_html=True)

st.divider()
# Fungsi untuk memuat data dengan caching
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Fungsi untuk membersihkan data
def clean_data(data, start_col=1):
    for col in data.columns[start_col:]:
        data[col] = data[col].astype(str).str.extract(r'(\d+)').astype(float)
    return data

# Load data
data1 = load_data("C3. layanan mahasiswa-prep.csv")

# Calculate average scores for each question
avg_scores = data1.mean()

# Prepare the indicator names (letters for X-axis)
questions = data1.columns.tolist()  # Assuming questions are column names
letters = [chr(i) for i in range(97, 97 + len(avg_scores))]  # ['a', 'b', 'c', ...]

# Create a DataFrame with letters as 'Indikator', average scores, and questions
avg_scores_df = pd.DataFrame({
    'Indikator': letters,
    'Pertanyaan': questions,
    'Rata-Rata Skor': avg_scores.values
})

col1, col2, col3 = st.columns(3)

        # Calculate metrics
min_score = avg_scores_df['Rata-Rata Skor'].min()
max_score = avg_scores_df['Rata-Rata Skor'].max()
mean_score = avg_scores_df['Rata-Rata Skor'].mean()

    
    # Display metrics with individual borders
st.markdown("""<style>
    .metric-box {
        text-align: center;
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #f5bf4a ;
    }
    .metric-box h3 {
        margin: 0;
        font-size: 1.5rem;
        color: black;
    }
    .metric-box p {
        margin: 5px 0 0;
        font-size: 1rem;
        color: black ;
    }
    </style>""", unsafe_allow_html=True)
with col1:
        st.markdown("""<div class="metric-box">
            <h3>{:.2f}</h3>
            <p>Minimum Skor</p>
        </div>""".format(min_score), unsafe_allow_html=True)
with col2:
        st.markdown("""<div class="metric-box">
            <h3>{:.2f}</h3>
            <p>Rata-Rata Skor</p>
        </div>""".format(mean_score), unsafe_allow_html=True)
with col3:
        st.markdown("""<div class="metric-box">
            <h3>{:.2f}</h3>
            <p>Maksimum Skor</p>
        </div>""".format(max_score), unsafe_allow_html=True)

selected_question_index = st.selectbox("Pilih Pertanyaan", range(len(questions)), format_func=lambda x: questions[x])

# Get the average score for the selected question
selected_question_avg_score = avg_scores_df['Rata-Rata Skor'].iloc[selected_question_index]
fulfilled_percentage = (selected_question_avg_score / 5) * 100
not_fulfilled_percentage = 100 - fulfilled_percentage


col1, col2, = st.columns(2)
with col1:
    st.data_editor(
                avg_scores_df,
                column_config={
                    "Rata-Rata Skor": st.column_config.ProgressColumn(
                        "Rata-Rata Skor",
                        help="Skor rata-rata berdasarkan indikator",
                        format="{:.2f}",  # Format angka dengan 2 desimal
                        min_value=0,  # Skor minimal
                        max_value=5,  # Skor maksimal (asumsi skor 1-5)
                    ),
                },
                hide_index=True,
                use_container_width=True  # Menggunakan lebar kontainer penuh untuk tabel
            )

with col2:
           # Line Chart for the average scores of each indicator
    fig_line = px.line(
        avg_scores_df,
        x='Indikator',
        y='Rata-Rata Skor',
        labels={'Indikator': 'Indikator', 'Rata-Rata Skor': 'Rata-Rata Skor'},
        title="Perubahan Skor Rata-Rata untuk Setiap Indikator",
        markers=True
    )

    # Update the line color to use the sunset color scale
    fig_line.update_traces(
        line=dict(color='rgba(255, 99, 71, 1)'),  # Default line color if you want specific color
        marker=dict(color=avg_scores_df['Rata-Rata Skor'], colorscale='sunset')  # Applying color scale to markers
    )

    # Update layout for line chart
    fig_line.update_layout(
        title_x=0.2,  # Centers the title
        title_y=0.95,  # Adjusts the title position vertically
        title_font=dict(size=20, color="white"),  # Title font size and color
        xaxis_title="Indikator",
        yaxis_title="Rata-Rata Skor",
        xaxis=dict(
            tickmode='array', 
            tickvals=avg_scores_df['Indikator'],  # Use the actual indicator names for ticks
            showgrid=True,
            gridcolor='#cecdcd',  # Light grid color for x-axis
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#cecdcd',  # Light grid color for y-axis
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        font=dict(color='#cecdcd'),  # Font color for the chart
    )

    # Display the line chart
    st.plotly_chart(fig_line)
    


# Prepare data for the donut chart
fulfillment_data = pd.DataFrame({
    'Status': ['Terpenuhi', 'Tidak Terpenuhi'],
    'Persentase': [fulfilled_percentage, not_fulfilled_percentage]
})

# Membuat layout kolom
col1, col2, col3 = st.columns(3)


with col1:
    # Create the donut chart
    fig_donut = px.pie(
        fulfillment_data,
        values='Persentase',
        names='Status',
        hole=0.4,
        title=f"Persentase Terpenuhi dan Tidak Terpenuhi untuk Pertanyaan",
        color_discrete_sequence=px.colors.sequential.Sunset
    )
    # Update layout to center the title and position the legend at the bottom
    fig_donut.update_layout(
        title_x=0,  # Centers the title
        legend_title="Indikator",  # Title for the legend
        legend_orientation="h",  # Horizontal legend
        legend_yanchor="bottom",  # Aligns legend at the bottom
        legend_y=-0.4,  # Moves the legend below the chart
        legend_x=0.4,  # Centers the legend horizontally
        legend_xanchor="right"  # Ensures that the legend is anchored in the center
    )
    # Display the donut chart
    st.plotly_chart(fig_donut)


with col2:
    
    # Create a donut chart for score distribution
    fig_donut = px.pie(
        avg_scores_df,
        values='Rata-Rata Skor',
        hole=0.4,
        title="Distribusi Skor Rata-Rata Per Indikator",
        color_discrete_sequence=px.colors.sequential.Sunset
    )

    # Update layout to center the title and position the legend at the bottom
    fig_donut.update_layout(
        title_x=0,  # Centers the title
        legend_title="Indikator",  # Title for the legend
        legend_orientation="h",  # Horizontal legend
        legend_yanchor="bottom",  # Aligns legend at the bottom
        legend_y=1,  # Moves the legend below the chart
        legend_x=0.4,  # Centers the legend horizontally
        legend_xanchor="center"  # Ensures that the legend is anchored in the center
    )
    # Display the donut chart
    st.plotly_chart(fig_donut)

with col3:
 
    # Plot a bar chart for average scores
    fig_bar = px.bar(
        avg_scores_df,
        x='Indikator',
        y='Rata-Rata Skor',
        labels={'Indikator': 'Indikator', 'Rata-Rata Skor': 'Rata-Rata Skor'},
        title="Rata-Rata Skor untuk Setiap Indikator",
        color='Rata-Rata Skor',
        color_continuous_scale='sunset',
        height=400,
        hover_data=["Rata-Rata Skor"]  # Include only non-conflicting fields
    )
            # Mengatur posisi judul agar berada di tengah
    fig_bar.update_layout(
        title_x=0.2  # Menempatkan judul di tengah (0.5 artinya di tengah dari grafik)
    )

    # Display the bar chart
    st.plotly_chart(fig_bar)











