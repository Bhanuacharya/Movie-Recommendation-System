import pickle
from altair.vegalite.v4.schema.channels import Column
import streamlit as st
import requests
from streamlit.elements import text
from streamlit_player import st_player
import json


st.header('Movies in Trending💥💥')
response_API = requests.get('https://api.themoviedb.org/3/trending/movie/week?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
data = response_API.text
parse_json = json.loads(data)
poster_path1 = parse_json['results'][0]['poster_path']
poster_path2=parse_json['results'][1]['poster_path']
poster_path3=parse_json['results'][2]['poster_path']
poster_path4=parse_json['results'][3]['poster_path']
poster_path5=parse_json['results'][4]['poster_path']
Trending_movie_path1="https://image.tmdb.org/t/p/w500/" + poster_path1
Trending_movie_path2="https://image.tmdb.org/t/p/w500/" + poster_path2
Trending_movie_path3="https://image.tmdb.org/t/p/w500/" + poster_path3
Trending_movie_path4="https://image.tmdb.org/t/p/w500/" + poster_path4
Trending_movie_path5="https://image.tmdb.org/t/p/w500/" + poster_path5
col1, col2,col3,col4,col5 = st.columns(5)
with col1:
    st.image(Trending_movie_path1)
with col2:
    st.image(Trending_movie_path2)
with col3:
    st.image(Trending_movie_path3)
with col4:
    st.image(Trending_movie_path4)
with col5:
    st.image(Trending_movie_path5)


with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

st.header('Movie Recommendation System')
movies = pickle.load(open("movies_dict.pkl", 'rb'))

similarity = pickle.load(open("similarity1.pkl", 'rb'))

movie_list = movies['title']
# st.write(movie_list)
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

#st.write(selected_movie)

movie_index = movies[movies['title'] == selected_movie]
id_give = (movie_index['movie_id']).index[0]


index1 = movies[movies['title'] == selected_movie]
abc_id=(index1['movie_id'][id_give])


#st.write(abc_id)

#st.write(movies['title'])



url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(abc_id)
re = requests.get(url)
re = re.json()
poster_path = re['poster_path']
full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
give_genre = re['genres']


def fetch_poster(id_give):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        id_give)
    re = requests.get(url)
    re = re.json()
    poster_path = re['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path



col1, col2 = st.columns([1, 2])
with col1:
    st.image(full_path)

with col2:
    st.subheader(re['original_title'])
    st.caption(f"Genre: {give_genre} Year: {re['release_date']}")
    st.write(re['overview'])
    st.text(f"Rating: {re['vote_average']}")
    st.progress(float(re['vote_average']) / 10)


def video_player(id_give):
    for_video = "https://api.themoviedb.org/3/movie/{}/videos?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(abc_id)
    rv = requests.get(for_video)
    rv = rv.json()

    for_key = rv["results"][0]

    youtube_key =for_key['key']

    link_youtube = ("https://youtu.be/{}").format(youtube_key)

    return link_youtube


st_player(video_player(abc_id))





def recommend(movie):
    # st.button("recommend")
    movie_index = movies[movies['title'] == movie]

    distance = sorted(list(enumerate(similarity[id_give])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []

    recommended_movie_posters = []

    recommended_movie_id=[]



    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_id.append(movies.iloc[i[0]].movie_id)
    return recommended_movie_names, recommended_movie_posters,recommended_movie_id


if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters,recommended_movie_id = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        movie1 = recommended_movie_names[0]
        st.text(movie1)
        st.image(recommended_movie_posters[0])


    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
