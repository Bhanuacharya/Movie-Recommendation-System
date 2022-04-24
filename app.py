import pickle
from IPython.core.display import display
from altair.vegalite.v4.schema.channels import Column
import streamlit as st
import requests
from streamlit.elements import text

from streamlit.proto.Video_pb2 import Video
from streamlit_player import st_player

st.header('Movie Recommendation System')

movies = pickle.load(open("new_data.pkl", 'rb'))

similarity = pickle.load(open("new_similarity.pkl", 'rb'))

movie_list = movies['title']

selected_movie = st.selectbox("Select a movie ", movie_list)




def select_movie(selected_movie):
    movie_index = movies[movies['title'] == selected_movie]
    id_give = (movie_index['id']).index[0]
    index1 = movies[movies['title'] == selected_movie]
    index_movie=(index1['id'][id_give])

    return id_give , index_movie

id_give , index_movie = select_movie(selected_movie)


def video_player(index_movie):
    for_video = "https://api.themoviedb.org/3/movie/{}/videos?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(index_movie)
    rv = requests.get(for_video)
    rv = rv.json()

    for_key = rv["results"][0]

    youtube_key =for_key['key']

    link_youtube = ("https://youtu.be/{}").format(youtube_key)

    return link_youtube


st_player(video_player(index_movie))


url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(index_movie)
re = requests.get(url)
re = re.json()
poster_path = re['poster_path']
full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

movie_genre = re['genres']
give_date = re['release_date']

# st.markdown(
#     """
#     <style>
#     .reportview-container {
#         background: url("https://image.tmdb.org/t/p/w500//cnQp8GmOWahIgQaH60Kwez3TNzw.jpg")
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )


def get_gerna(movie_genre):
    values = []
    items_val = []
    #single_val = []
    for a in movie_genre:
        for k, v in a.items():
            values.append(v)

    for items in values:
        if(type(items) == str):
            items_val.append(items)
    
    return items_val



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
    st.caption(f"Genre: {get_gerna(movie_genre)}")
    st.caption(f"Year: {give_date}")
    st.write(re["overview"])
    st.text(f"Rating: {re['vote_average']}")
    st.progress(float(re['vote_average']) / 10)



def recommend(movie):
    # st.button("recommend")
    movie_index = movies[movies['title'] == movie]

    distance = sorted(list(enumerate(similarity[id_give])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []

    recommended_movie_posters = []

    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        
        movie1 = recommended_movie_names[0]
        st.text(movie1)
        st.image(recommended_movie_posters[0])
        if st.button("like this "):
            st.write(movie1)

            
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


# if st.button('Show Recommendation'):
#     recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
#     with col1:
#         movie_1 = (recommended_movie_names[0])
#         id_give , index_movie = select_movie(movie_1)
#         st.write(id_give,index_movie)
#         st.write(movie_1)
#         recommended_movie_names1 = recommend(movie_1)
       


