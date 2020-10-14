<template>
    <div class="nav-wrap">
        <div class="item" :class="{ active: active === 'home' }"><a href="#" @click="click('home')">Home</a></div>
        <div v-if="isLogin" class="item" :class="{ active: active === 'tool' }"><a href="#" @click="click('tool')">Tools</a></div>
        <div v-if="isLogin" class="item" :class="{ active: active === 'file' }"><a href="#" @click="click('file')">Files</a></div>
        <div class="item" :class="{ active: active === 'result' }"><a href="#" @click="click('result')">Results</a></div>
    </div>
</template>

<script>
export default {
    props: {
        tab: {
            type: String,
            default: true,
        },
        login: {
            type: Boolean,
            default: false
        }
    },
    watch: {
        tab(newVal) {
            this.click(this.tab)
        },
        login(newVal) {
            console.log(newVal)
            this.isLogin = newVal
        }
    },
    data() {
        return {
            isLogin: false,
            active: this.tab
        };
    },
    created () {
        this.isLogin = this.login
        console.log(this.login)
    },
    methods: {
        click(val) {
            this.active = val;
            this.$emit('change', val);
        }
    }
}
</script>

<style scoped>
.nav-wrap {
    width: 200px;
    padding: 40px 20px;
}
.nav-wrap .item {
    line-height: 60px;
    font-size: 20px;
    padding-left: 40px;
    font-weight: bold;
}
.nav-wrap .item a {
    color: #ccc;
}
.nav-wrap .active a {
    color: #555;
}
.main-wrap {
    width: calc(100% - 560px);
    padding: 40px 20px;
    border-left: 1px solid #ccc;
    border-right: 1px solid #ccc;
}
.twitter-wrap {
    width: 360px;
    padding: 40px 20px;
}
</style>