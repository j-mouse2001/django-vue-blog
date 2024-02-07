<template>
    <div v-for="article in info.results" v-bind:key="article.url" id="articles">
        <div>
            <span
                  v-for="tag in article.tags"
                  v-bind:key="tag"
                  class="tag"
            >
                {{ tag }}
            </span>
        </div>
<!--        <div class="article-title">-->
<!--            {{ article.title }}-->
<!--        </div>-->
            <router-link
                :to="{ name: 'ArticleDetail', params: { id: article.id }}"
                class="article-title"
            >
            {{ article.title }}
            </router-link>
        <div>{{ formatted_time(article.created) }}</div>
    </div>

    <div id="paginator">
        <span v-if="is_page_exists('previous')">
            <router-link :to="get_path('previous')">
                Prev
            </router-link>
        </span>
        <span class="...e">
            ...
        </span>
        <span v-if="is_page_exists('next')">
            <router-link :to="get_path('next')">
                Next
            </router-link>
        </span>
    </div>

</template>

<script>
    import axios from 'axios';

    export default {
        name: 'ArticleList',
        data: function () {
            return {
                info: ''
            }
        },
        mounted() {
            this.get_article_data()
        },
        methods: {
            formatted_time: function (iso_date_string) {
                const date = new Date(iso_date_string);
                return date.toLocaleDateString()
            },

            is_page_exists(direction) {
                if (direction === 'next') {
                    return this.info.next !== null
                }
                return this.info.previous !== null
            },

            get_path: function (direction) {
                let url = '';

                try {
                    switch (direction) {
                        case 'next':
                            if (this.info.next !== undefined) {
                                url += (new URL(this.info.next)).search
                            }
                            break;
                        case 'previous':
                            if (this.info.previous !== undefined) {
                                url += (new URL(this.info.previous)).search
                            }
                            break;
                    }
                }
                catch { return url }

                return url
            },

            get_article_data: function () {
                let url = '/api/article';

                let params = new URLSearchParams();
                // 注意 appendIfExists 方法是原生没有的
                // 原生只有 append 方法，但此方法不能判断值是否存在
                params.appendIfExists('page', this.$route.query.page);
                params.appendIfExists('search', this.$route.query.search);

                const paramsString = params.toString();
                if (paramsString.charAt(0) !== '') {
                    url += '/?' + paramsString
                }

                axios
                    .get(url)
                    .then(response => (this.info = response.data))
            }
        },

        watch: {
            // 监听路由是否有变化
            $route() {
                this.get_article_data()
            }
        }
    }

</script>

<!-- "scoped" 使样式仅在当前组件生效 -->
<style scoped>
    #articles {
        padding: 10px;
    }

    .article-title {
        font-size: large;
        font-weight: bolder;
        color: black;
        text-decoration: none;
        padding: 5px 0 5px 0;
    }

    .tag {
        padding: 2px 5px 2px 5px;
        margin: 5px 5px 5px 0;
        font-family: Georgia, Arial, sans-serif;
        font-size: small;
        background-color: #4e4e4e;
        color: whitesmoke;
        border-radius: 5px;
    }

    #paginator {
        text-align: center;
        padding-top: 50px;
    }

    a {
        color: black;
    }

    .current-page {
        font-size: x-large;
        font-weight: bold;
        padding-left: 10px;
        padding-right: 10px;
    }
</style>