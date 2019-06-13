var vm = new Vue({
    el: '#app',
      // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host,
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        order_id: '',
        skus: [],

    },
    mounted: function(){
        this.order_id = this.get_query_string('order_id');
        axios.get(this.host+'/orders/'+this.order_id+'/uncommentgoods/', {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json'
            })
            .then(response => {
                this.skus = response.data.skus;
                for(var i=0;i<this.skus.length;i++){
                    this.skus[i].url = '/goods/' + this.skus[i].id + '.html';
                    Vue.set(this.skus[i], 'score', 0); // 记录随鼠标变动的星星数
                    Vue.set(this.skus[i], 'display_score', 0); // 展示变动的分数值
                    this.skus[i].final_score = 0; // 记录用户确定的星星数
                    Vue.set(this.skus[i], 'comment', '');
                    Vue.set(this.skus[i], 'is_anonymous', false);
                }
            })
            .catch(error => {
                console.log(error.response.data);
            })
    },
    methods: {
            getCookie: function (cname) {
            var name = cname + "=";
             var ca = document.cookie.split(';');
            console.log("获取cookie,现在循环")
            for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            console.log(c)
             while (c.charAt(0) == ' ') c = c.substring(1);
            if (c.indexOf(name) != -1){
             return c.substring(name.length, c.length);
            }
            }
            return "";},

        // 退出
        logout: function(){
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },
        // 获取url路径参数
        get_query_string: function(name){
            var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
            var r = window.location.search.substr(1).match(reg);
            if (r != null) {
                return decodeURI(r[2]);
            }
            return null;
        },
        on_stars_mouseover: function(index, score){
            this.skus[index].score = score;
            this.skus[index].display_score = score * 20;
        },
        on_stars_mouseout: function(index) {
            this.skus[index].score = this.skus[index].final_score;
            this.skus[index].display_score = this.skus[index].final_score * 20;
        },
        on_stars_click: function(index, score) {
            this.skus[index].final_score = score;
        },
        save_comment: function(index){
            var sku = this.skus[index];
            //修改
            if (sku.comment.length < 5 && sku.comment.length !== 0 ){
                alert('请填写多余5个字的评价内容');
            } else {
                axios.post(this.host+'/orders/'+this.order_id+'/comments/', {
                        order: this.order_id,
                        sku: sku.sku_id,
                        comment: sku.comment,
                        score: sku.final_score,
                        is_anonymous: sku.is_anonymous,
                    }, {
                        headers: {
                            'X-CSRFToken':this.getCookie('csrftoken'),   //
                            // 'Authorization': 'JWT ' + this.token
                        },
                        responseType: 'json'
                    })
                    .then(response => {
                        this.skus.splice(index, 1);
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
        }
    }
});