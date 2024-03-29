import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title = 'Capstone Project Tetris Batch 4',
    layout='wide'
)



st.sidebar.header('Open Mindset')
video_file = open('data.mp4', 'rb')
video_bytes = video_file.read()
st.sidebar.video(video_bytes)
st.sidebar.markdown("[Gita Irawan Wirjawan, B.B.A., M.B.A., M.P.A.](https://www.youtube.com/shorts/3B7gpUSPIDU)")


st.title('Populasi No 4 di Dunia, Jumlah Pelajar Internasional _Tidak Masuk_ Top 20.')
st.caption("Oleh: Muhammad Dzikry Afandi")
# st.header("Gambaran mahasiswa internasional, Indonesia.")


col1, col2 =  st.columns([2,3])
with col1:
  st.subheader("Latar Belakang")
  st.markdown("Dengan semakin terbukanya kesempatan untuk menempuh pendidikan di luar negeri, khususnya di perguruan tinggi terbaik dunia, para pelajar di negara berkembang tentunya memiliki peluang yang besar untuk merasakan kualitas pendidikan tinggi yang setara.")
  # st.markdown("Dalam era globalisasi pendidikan, pelajar dari negara berkembang semakin melihat peluang yang besar dalam menempuh pendidikan di perguruan tinggi terbaik dunia. Fenomena ini didorong oleh persepsi akan kualitas pendidikan tinggi yang tinggi, standar akademik yang unggul, dan fasilitas pendidikan yang modern. Gelar dari universitas terkemuka dianggap sebagai investasi dalam karier masa depan, membuka pintu untuk peluang kerja yang lebih baik. Faktor-faktor ini, bersama dengan kemudahan akses dan mobilitas internasional, menjadikan opsi pendidikan di luar negeri sebagai pilihan menarik bagi para pelajar di negara berkembang yang mencari pengalaman pendidikan tinggi yang berkualitas.")

with col2:
  st.subheader("Projek Objektif")
  st.markdown("Projek ini bertujuan untuk menganalisis persebaran mahasiswa internasional di universitas-universitas terkemuka di seluruh dunia, termasuk jumlah mahasiswa Indonesia yang berkuliah di luar negeri setiap tahun. Dengan analisis ini, kami ingin memberikan pemahaman yang lebih baik tentang negara dan universitas yang menjadi tujuan utama mahasiswa internasional, tren perkembangan mahasiswa di universitas-universitas terbaik, serta jumlah dan tren pertumbuhan mahasiswa Indonesia di luar negeri. Kami berharap hasil analisis ini dapat memberikan wawasan yang berharga bagi pemerintah dalam merancang kebijakan untuk mendorong pertumbuhan mahasiswa internasional asal Indonesia, serta langkah-langkah untuk meningkatkan partisipasi dan akses pendidikan tinggi internasional bagi masyarakat Indonesia.")

st.subheader("Key Questions")
st.markdown('''
            - Apa saja universitas terkemuka di seluruh dunia yang menjadi tujuan utama mahasiswa internasional, dan bagaimana persebaran mereka menurut wilayah geografis?
            - Bagaimana tren jumlah mahasiswa internasional di universitas-universitas terbaik selama beberapa tahun terakhir?
            - Berapa jumlah mahasiswa Indonesia yang berkuliah di luar negeri setiap tahunnya, bagaimana perbandingannya dengan negara negara tetangga?
            - Apa saja negara tujuan utama bagi mahasiswa Indonesia yang berkuliah di luar negeri, dan bagaimana tren persebaran mereka dalam beberapa tahun terakhir?
''')

st.write('')
st.write('')
st.write('')
st.write('')
st.subheader("Persebaran Peringkat Universitas Dunia")


# ------------------------SCATTER PLOT 1 ------------------------
univ_inworld = pd.read_csv('./data/Jumlah Universitas tiap negara.csv')
data = univ_inworld[['NO','COUNTRY','TOP 100','101-500','501-1000','1001-5000','5001-10000','10001-n','TOTAL']]

# Pilihan kategori
options = ['TOP 100', '101-500', '501-1000', '1001-5000', '5001-10000','10001-n', 'TOTAL']

col1, col2 =  st.columns([1,4])

with col1:
  st.write("")
  st.write("")
  st.write("")
  selected_category = st.radio("Pilih kategori:", options)

with col2:
  top_countries = univ_inworld.nlargest(10, selected_category)

  fig = px.scatter(top_countries, y='COUNTRY', x='TOTAL',
                 size=selected_category, 
                 color=selected_category,
                 hover_name='COUNTRY', 
                 hover_data=['TOP 100','101-500','501-1000','1001-5000','5001-10000','10001-n'],
                 labels={'TOTAL': 'Total Universitas', 'COUNTRY': 'Negara'})
  st.plotly_chart(fig)

st.markdown("Menurut Webometrics [1](https://www.webometrics.info/en/distribution_by_country), Amerika Serikat menjadi negara yang memiliki **jumlah universitas terbanyak** di setiap kategori")
st.markdown("Yang menarik dari 32018 univeristas, Amerika juga memiliki 1569 univeristas yang berada diperingkat 5001-10000 itu merupakan 49.34% dari seluruh universitas di Amerika, jika ditambahkan data dari peringkat 10000-32018 maka persentasenya naik sampai 73.63%. Ini juga menandakan bahwa tidak semua universitas di Amerika ada diperingkat atas, masih ada 3/4 universitas yang berada diperingkat bawah.")
st.markdown("Alih alih fokus ke peringkat bawah, penguasaan Amerika serikat terhadap **separuh lebih** di top 100 tentulah lebih mengagumkan. pesaing terdekatnya yaitu britania raya hanya sanggup memasukkan 8 universitasnya ke top 100.")

st.subheader("Persaingan Peringkat 10 Besar Dunia")


# ------------------------Line Chart------------------------
# Membaca data
rank_univ = pd.read_csv('./data/rankUniv.csv')

data = rank_univ[['NO','Tahun','Rank','Nama','Region/Country']]

# Mengambil nilai unik peringkat
min_rank = int(data['Rank'].min())
max_rank = int(data['Rank'].max())

# Widget slider untuk memilih peringkat
selected_rank = st.slider("Pilih Peringkat", min_value=min_rank, max_value=max_rank, value=(min_rank, min(min_rank+4, max_rank)))

# Filtering data untuk hanya mengambil peringkat terpilih
filtered_data = data[data['Rank'].between(selected_rank[0], selected_rank[1])]

# Pivot the data to have years as columns
pivot_data = filtered_data.pivot_table(index='Nama', columns='Tahun', values='Rank', aggfunc='first')

# Plotting line chart
fig = px.line(pivot_data.T,  # Transpose pivot_data so that years become x-axis
              labels={'value': 'Ranking', 'index': 'Year', 'variable': 'University'}
             )

# Menambahkan mode 'lines+markers' untuk menampilkan titik pada setiap data
fig.update_traces(mode='lines+markers')


# Mengatur ketebalan garis
for trace in fig.data:
    trace.line.width = 2  # Menetapkan ketebalan garis menjadi 2 px

# Menampilkan plot
st.plotly_chart(fig, use_container_width=True, width=None, height=600)


st.markdown('''Berbanding lurus dengan dominasi Amerika serikat, 3 dari top 5 berasal dari negara Amerika, 7 dari top 10 juga diisi oleh negara tersebut. Namun University of Oxford, United states masihlah **konsisten dipuncak** selama 7 tahun belakangan ini.[2](https://www.timeshighereducation.com/world-university-rankings/2024/world-ranking)

Ini menarik, berikut adalah persebaran mahasiswa internasional dari beberapa univeristas yang masuk kedalam 10 universitas terbaik''')


with st.expander("University of California, Berkeley"):
  df_california = pd.read_csv('./data/california.csv')
  data = df_california[['Year','Student','Country']]

  # Grouping data by Year and Country and summing up Student
  grouped_data = data.groupby(['Year', 'Country']).sum().reset_index()
  last_year_data = grouped_data[grouped_data['Year'] == grouped_data['Year'].max()]

  # Menentukan top countries berdasarkan jumlah mahasiswa pada tahun terakhir
  top_countries = last_year_data.groupby('Country')['Student'].sum().nlargest(10).index

  # Filtering data untuk hanya mengambil data dari negara dengan peringkat pertama
  top_country = top_countries[0]  # Mengambil negara dengan peringkat pertama
  rank1 = grouped_data[grouped_data['Country'] == top_country]

  # Memperbarui opsi yang tersedia dalam selectbox
  selected_country = st.selectbox("Pilih negara pembanding", rank1['Country'].unique(), key="cali_selectbox")

  # Filtering data for the selected countries
  filtered_data = grouped_data[grouped_data['Country'].isin(top_countries) | (grouped_data['Country'] == selected_country)]

  # Creating line chart
  fig = px.line(filtered_data, x='Year', y='Student', color='Country', title='Jumlah mahasiswa Berkeley berdasarkan negara selama beberapa tahun')

  for i, country in enumerate(fig.data):
    rank = list(top_countries).index(country.name) + 1
    country.name = f"(Rank {rank}) {country.name}"

  fig.update_traces(mode='lines+markers')
  st.plotly_chart(fig, use_container_width=True, width=None, height=600)
  st.markdown("Sumber: [University of California, Berkeley](https://internationaloffice.berkeley.edu/about-us/statistics/enrollment_data)")


with st.expander("University of Cambridge"):
  df_cambridge = pd.read_csv('./data/cambridge.csv')

  # cambridge
  data = df_cambridge[['Year','Student','Country']]

  # Grouping data by Year and Country and summing up Student
  grouped_data = data.groupby(['Year', 'Country']).sum().reset_index()
  
  last_year_data = grouped_data[grouped_data['Year'] == grouped_data['Year'].max()]

  # Menentukan top countries berdasarkan jumlah mahasiswa pada tahun terakhir
  top_countries = last_year_data.groupby('Country')['Student'].sum().nlargest(10).index

  # Filtering data untuk hanya mengambil data dari negara dengan peringkat pertama
  top_country = top_countries[0]  # Mengambil negara dengan peringkat pertama
  rank1 = grouped_data[grouped_data['Country'] == top_country]

  # Memperbarui opsi yang tersedia dalam selectbox
  selected_country = st.selectbox("Pilih negara pembanding", rank1['Country'].unique(), key="cam_selectbox")

  # Filtering data for the selected countries
  filtered_data = grouped_data[grouped_data['Country'].isin(top_countries) | (grouped_data['Country'] == selected_country)]

  # Creating line chart
  fig = px.line(filtered_data, x='Year', y='Student', color='Country', title='Jumlah mahasiswa Cambridge berdasarkan negara selama beberapa tahun')

  for i, country in enumerate(fig.data):
    rank = list(top_countries).index(country.name) + 1
    country.name = f"(Rank {rank}) {country.name}"

  fig.update_traces(mode='lines+markers')
  st.plotly_chart(fig, use_container_width=True, width=None, height=600)
  st.markdown("Sumber: [University of Cambridge](https://www.internationalstudents.cam.ac.uk/applying/global-community/international-student-data)")


with st.expander("Massachusetts Institute of Technology"):
  df_mit =   pd.read_csv('./data/mit.csv')

  # mit
  data = df_mit[['Year','Student','Country']]
 
  # Grouping data by Year and Country and summing up Student
  grouped_data = data.groupby(['Year', 'Country']).sum().reset_index()
  
  last_year_data = grouped_data[grouped_data['Year'] == grouped_data['Year'].max()]

  # Menentukan top countries berdasarkan jumlah mahasiswa pada tahun terakhir
  top_countries = last_year_data.groupby('Country')['Student'].sum().nlargest(10).index

  # Filtering data untuk hanya mengambil data dari negara dengan peringkat pertama
  top_country = top_countries[0]  # Mengambil negara dengan peringkat pertama
  rank1 = grouped_data[grouped_data['Country'] == top_country]

  # Memperbarui opsi yang tersedia dalam selectbox
  selected_country = st.selectbox("Pilih negara pembanding (MIT)", rank1['Country'].unique(), key="mit_selectbox")

  # Filtering data for the selected countries
  filtered_data = grouped_data[grouped_data['Country'].isin(top_countries) | (grouped_data['Country'] == selected_country)]

  # Creating line chart
  fig = px.line(filtered_data, x='Year', y='Student', color='Country', title='Jumlah mahasiswa MIT berdasarkan negara selama beberapa tahun')

  for i, country in enumerate(fig.data):
      rank = list(top_countries).index(country.name) + 1
      country.name = f"(Rank {rank}) {country.name}"

  fig.update_traces(mode='lines+markers')
  st.plotly_chart(fig, use_container_width=True, width=None, height=600)
  st.markdown("Sumber: [Massachusetts Institute of Technology](https://iso.mit.edu/about-iso/statistics/)")

with st.expander("Princeton University"):
  df_princeton =   pd.read_csv('./data/princeton.csv')

  # princeton
  data = df_princeton[['Year','Student','Country']]

  # Grouping data by Year and Country and summing up Student
  grouped_data = data.groupby(['Year', 'Country']).sum().reset_index()
  
  last_year_data = grouped_data[grouped_data['Year'] == grouped_data['Year'].max()]

  # Menentukan top countries berdasarkan jumlah mahasiswa pada tahun terakhir
  top_countries = last_year_data.groupby('Country')['Student'].sum().nlargest(10).index

  # Filtering data untuk hanya mengambil data dari negara dengan peringkat pertama
  top_country = top_countries[0]  # Mengambil negara dengan peringkat pertama
  rank1 = grouped_data[grouped_data['Country'] == top_country]

  # Memperbarui opsi yang tersedia dalam selectbox
  selected_country = st.selectbox("Pilih negara pembanding", rank1['Country'].unique(), key="prin_selectbox")

  # Filtering data for the selected countries
  filtered_data = grouped_data[grouped_data['Country'].isin(top_countries) | (grouped_data['Country'] == selected_country)]

  # Creating line chart
  fig = px.line(filtered_data, x='Year', y='Student', color='Country', title='Jumlah mahasiswa Princeton berdasarkan negara selama beberapa tahun')

  for i, country in enumerate(fig.data):
    rank = list(top_countries).index(country.name) + 1
    country.name = f"(Rank {rank}) {country.name}"

  fig.update_traces(mode='lines+markers')
  st.markdown("Sumber: [Princeton University](https://davisic.princeton.edu/about-us/statistics)")

  st.plotly_chart(fig, use_container_width=True, width=None, height=600)

with st.expander("Yale University"):
  df_yale =   pd.read_csv('./data/yale.csv')

  # yale
  data = df_yale[['Year','Student','Country']]

  # Grouping data by Year and Country and summing up Student
  grouped_data = data.groupby(['Year', 'Country']).sum().reset_index()

  
  last_year_data = grouped_data[grouped_data['Year'] == grouped_data['Year'].max()]

  # Menentukan top countries berdasarkan jumlah mahasiswa pada tahun terakhir
  top_countries = last_year_data.groupby('Country')['Student'].sum().nlargest(10).index

  # Filtering data untuk hanya mengambil data dari negara dengan peringkat pertama
  top_country = top_countries[0]  # Mengambil negara dengan peringkat pertama
  rank1 = grouped_data[grouped_data['Country'] == top_country]

  # Memperbarui opsi yang tersedia dalam selectbox
  selected_country = st.selectbox("Pilih negara pembanding", rank1['Country'].unique(), key="yale_selectbox")

  # Filtering data for the selected countries
  filtered_data = grouped_data[grouped_data['Country'].isin(top_countries) | (grouped_data['Country'] == selected_country)]

  # Creating line chart
  fig = px.line(filtered_data, x='Year', y='Student', color='Country', title='Jumlah mahasiswa Yale berdasarkan negara selama beberapa tahun')

  for i, country in enumerate(fig.data):
    rank = list(top_countries).index(country.name) + 1
    country.name = f"(Rank {rank}) {country.name}"

  fig.update_traces(mode='lines+markers')
  st.plotly_chart(fig, use_container_width=True, width=None, height=600)
  st.markdown("Sumber: [Yale Universit](https://oiss.yale.edu/about/statistics-reports-2022)")


with st.expander("University of Oxford"):
  df_oxford =   pd.read_csv('./data/oxford.csv')

  # oxford
  data = df_oxford[['Year','Student','Country']]

  # Grouping data by Year and Country and summing up Student
  grouped_data = data.groupby(['Year', 'Country']).sum().reset_index()

  
  last_year_data = grouped_data[grouped_data['Year'] == grouped_data['Year'].max()]

  # Menentukan top countries berdasarkan jumlah mahasiswa pada tahun terakhir
  top_countries = last_year_data.groupby('Country')['Student'].sum().nlargest(10).index

  # Filtering data untuk hanya mengambil data dari negara dengan peringkat pertama
  top_country = top_countries[0]  # Mengambil negara dengan peringkat pertama
  rank1 = grouped_data[grouped_data['Country'] == top_country]

  # Memperbarui opsi yang tersedia dalam selectbox
  selected_country = st.selectbox("Pilih negara pembanding", rank1['Country'].unique(), key="ox_selectbox")

  # Filtering data for the selected countries
  filtered_data = grouped_data[grouped_data['Country'].isin(top_countries) | (grouped_data['Country'] == selected_country)]

  # Creating line chart
  fig = px.line(filtered_data, x='Year', y='Student', color='Country', title='Jumlah mahasiswa Oxford berdasarkan negara selama beberapa tahun')

  for i, country in enumerate(fig.data):
    rank = list(top_countries).index(country.name) + 1
    country.name = f"(Rank {rank}) {country.name}"

  fig.update_traces(mode='lines+markers')
  st.plotly_chart(fig, use_container_width=True, width=None, height=600)
  st.markdown("Sumber: [University of Oxford](https://academic.admin.ox.ac.uk/student-statistics)")


with st.expander("Stanford University"):
  df_stanford =   pd.read_csv('./data/stanford.csv')

  # stanford
  data = df_stanford[['Year','Student','Country']]

  # Grouping data by Year and Country and summing up Student
  grouped_data = data.groupby(['Year', 'Country']).sum().reset_index()


  last_year_data = grouped_data[grouped_data['Year'] == grouped_data['Year'].max()]

  # Menentukan top countries berdasarkan jumlah mahasiswa pada tahun terakhir
  top_countries = last_year_data.groupby('Country')['Student'].sum().nlargest(10).index

  # Filtering data untuk hanya mengambil data dari negara dengan peringkat pertama
  top_country = top_countries[0]  # Mengambil negara dengan peringkat pertama
  rank1 = grouped_data[grouped_data['Country'] == top_country]

  # Memperbarui opsi yang tersedia dalam selectbox
  selected_country = st.selectbox("Pilih negara pembanding", rank1['Country'].unique(), key="stanf_selectbox")

  # Filtering data for the selected countries
  filtered_data = grouped_data[grouped_data['Country'].isin(top_countries) | (grouped_data['Country'] == selected_country)]

  # Creating line chart
  fig = px.line(filtered_data, x='Year', y='Student', color='Country', title='Jumlah mahasiswa Stanford berdasarkan negara selama beberapa tahun')

  for i, country in enumerate(fig.data):
    rank = list(top_countries).index(country.name) + 1
    country.name = f"(Rank {rank}) {country.name}"

  fig.update_traces(mode='lines+markers')
  st.plotly_chart(fig, use_container_width=True, width=None, height=600)
  st.markdown("Sumber: [Stanford University](https://bechtel.stanford.edu/engage-our-center/about-us/annual-report-and-studentscholar-statistics)")



st.markdown("Dari ketujuh universitas terbaik dunia tersebut, jumlah pelajar internasional semuanya dikuasai oleh **Negeri China**. nama nama yang sering muncul adalah India, Korea Selatan, Kanada, Australia, Prancis, Germany, Singapore, Jepang, Brazil, United Kingdom, dan Taiwan")
st.subheader("Bagaimana Indonesia?")
st.markdown("Lalu, berapa mahasiswa indonesia yang belajar di universitas-universitas tersebut?")




# Membaca data
df_all = pd.read_csv('./data/mahasiswaIndo.csv')

# Membuat line chart
fig = px.line(df_all, x='YEAR', y='Student', color='Universitas', hover_data=['Country'])

# Menambahkan garis rata-rata untuk setiap tahun
avg_student = df_all.groupby('YEAR')['Student'].mean().reset_index()
fig.add_trace(go.Scatter(x=avg_student['YEAR'], y=avg_student['Student'], mode='lines', name='Average'))

# Menambahkan dot di setiap data
for data in fig.data:
    data.update(mode='lines+markers')

# Menampilkan plot
st.plotly_chart(fig, use_container_width=True, height=600)


st.markdown("Terlihat bahwa **sedikit sekali** warga indonesia yang menempuh pendidikan di universitas univeritas terbaik dunia tersebut, hanya hitungan puluhan. **Rata-rata ditahun 2021 hanya 83 orang dan 60 di 2020**, paling banyak di tahun 2023 dengan jumlah 187 orang yang berlokasi di California University. Namun disisi lain, tren pertumbuhannya **cenderung meningkat**, terutama di Stanford University dan Oxford University.")

st.subheader("Berapa Mahasiswa Indonesia?")
st.markdown("Untuk melihat bagaimana posisi indonesia dibandingkan negara negara lainnya, berikut adalah persebaran mahasiswa internasional tiap tiap negara.")


# Membaca data
df_studentworldseris = pd.read_csv('./data/internationalStudent.csv')

# Filter 5 negara teratas
top_countries = df_studentworldseris.groupby('Country')['Value'].sum().nlargest(5).index

# Dropdown untuk memilih tahun dengan nilai default ke tahun terakhir
selected_year = st.selectbox("Pilih Tahun", df_studentworldseris['Year'].unique(), index=len(df_studentworldseris['Year'].unique())-1)

# Filter data berdasarkan tahun yang dipilih
df_selected_year = df_studentworldseris[df_studentworldseris['Year'] == selected_year]

# Ambil 5 negara teratas untuk tahun yang dipilih
df_top_5 = df_selected_year[df_selected_year['Country'].isin(top_countries)]

# Hitung peringkat Indonesia
indonesia_rank = df_selected_year[df_selected_year['Country'] == 'Indonesia']['row_num'].iloc[0]

# Tambahkan data Indonesia ke dalam DataFrame
df_indonesia = pd.DataFrame({
    'Country': ['Indonesia'],
    'Year': [selected_year],
    'Value': [df_selected_year[df_selected_year['Country'] == 'Indonesia']['Value'].sum()],
    'row_num': [indonesia_rank]
})

# Gabungkan data negara teratas dengan Indonesia
df_combined = pd.concat([df_top_5, df_indonesia])
# Mengurutkan data berdasarkan nilai-nilai mereka
df_combined_sorted = df_combined.sort_values(by='Value')

# Membuat plot menggunakan Plotly
fig = go.Figure()

for index, row in df_combined_sorted.iterrows():
    color = 'blue' if row['Country'] == 'Indonesia' else 'gray'  # Tentukan warna untuk setiap negara
    fig.add_trace(go.Bar(x=[row['Value']], 
                         y=[row['Country']], 
                         name=row['Country'], 
                         orientation='h',
                         text=f'Rank: {row["row_num"]}, Value: {row["Value"]}',
                         marker=dict(color=color)))  # Beri warna pada bar

# Menambahkan layout
fig.update_layout(title=f'Rangking mahasiswa Indonesia pada tahun {selected_year}',
                  xaxis_title='Jumlah Mahasiswa',
                  yaxis_title='Negara',
                  showlegend=False
                  )

# Menampilkan plot menggunakan streamlit
st.plotly_chart(fig, use_container_width=True)


st.markdown("Berdasarkan data dari UIS Unesco [3](http://data.uis.unesco.org/). indonesia per 2021 berada **diperingkat 24**, turun 6 peringkat dari tahun sebelumnya, dari 58.491 menjadi 45.896. sangat jauh apabila dibandingkan dengan India apalagi China. Hal ini tentunya perlu dipertanyakan, apakah masyarakat indonesia tidak mampu bersaing di kancah internasional?")

st.subheader("Kemana Mahasiswa Indonesia?")
st.markdown("Setelah melihat peringkat dan persebaran mahasiswa indonesia, menarik untuk ditelusuri kemana saja mahasiswa indonesia yang berkuliah di luar negeri ini menempuh pendidikan, ini bisa dijadikan proyeksi persebaran terbanyak tujuan mahasiswa internasional asal indonesia.")

# Memuat data dari file CSV
df_studentworldseris = pd.read_csv('./data/indonesianStudent.csv')

# Membuat tree map
fig = px.treemap(df_studentworldseris, path=['Time', 'Country'], values='Value')

# Menampilkan plot
st.plotly_chart(fig, use_container_width=True)

st.markdown("Terlihat bahwa **Australia** yang menjadi negara tujuan pelajar indonesia, 1 dari 4 mahasiswa internasional kita ada di sana, tempat kedua ada Malaysia diangka 9000-an. lalu baru Amerika Serikat.")

st.subheader("Insight")
st.markdown("""
            - Jumlah mahasiswa indonesia hanya % dari populasi, sebagai negara dengan populasi per 2021 sebesar 275 juta, mahaiswa asal indonesia di luar negeri hanya berjumlah 45 ribu.
            - universitas terbaik terpusat di negara amerika. 53 universitas di negara amerika masuk kedalam 100 universitas terbaik, 7 universitas di amerika juga masuk kedalam 10 universitas terbaik.
            - mahasiswa indonesia yang berada di universitas top 10 per tahun 2023 rata rata hanya 83 mahasiswa, naik dari tahun sebelumnya yang hanya 59 mahasiswa. 
            - destinasi utama pelajar internasional asal indonesia adalah Australia, Malaysia dan Amerika Serikat. 1 dari 4 pelajar internasional asal indonesia berada di australia
            - adanya trend pertumbuhan di california university dan oxford univesity. masing masing di tahun 2005 ada diangka 14 mahasiswa dan 10 mahasiswa, lalu di tahun 2023 masing masing menjadi 187 mahasiswa dan 100 mahasiswa.
            """)

st.subheader("Apa selanjutnya?")
st.markdown("""
            - pemahaman akan pentingnya pendidikan perlu digalakkan.
            - informasi ketersediaan pendanaan untuk biaya berkuliah di luar negeri.
            - faktor yang penghambat untuk berkuliah diluar negeri.
            - peluang yang tersedia.
""")

st.markdown('''Contact Me: afandiahmed24@gmail.com LinkedIn: [Muhammad Dzikry Afandi](https://www.linkedin.com/in/muhammaddzikryafandi/)''')

