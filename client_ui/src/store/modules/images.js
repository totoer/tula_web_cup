import axios from 'axios';

export default {
  namespaced: true,
  state: {
    list: [],
    offset: 0,
    limit: 10
  },
  mutations: {
    SET_LIST(state, list) { state.list = list; },
    APPEND_TO_LIST(state, list) { state.list = state.list.concat(list) },
    SET_OFFSET(state, offset) { state.offset = offset; },
    SET_LIMIT(state, limit) { state.limit = limit; }
  },
  actions: {
    fetch(context) {
      return new Promise((success) => {
        axios.get(`/api/?limit=${context.state.limit}&offset=${context.state.offset}`).then((response) => {
          if(context.state.offset == 0) {
            context.commit('SET_LIST', response.data);
          } else {
            context.commit('APPEND_TO_LIST', response.data);
          }

          success();

        }).catch((errorResponse) => { debugger })
      });
    },
    like(context, {image, value}) {
      return new Promise((success) => {
        axios.post(`/api/image_like/`, {image_id: image.id, value: value}).then((response) => {
          success();
        }).catch((errorResponse) => { debugger })
      });
    },
    upload(context, image) {
      return new Promise((success) => {
        let formData = new FormData();
        formData.append('image', image.files[0]);

        let config = {
          headers: {'Content-Type': 'multipart/form-data' }
        };

        axios.post('/api/', formData, config).then((response) => {
          success();
        }).catch((errorResponse) => { debugger; })
      });
    }
  },  
}