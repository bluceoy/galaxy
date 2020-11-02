<template>
    <div>
        <div class="header">
            <h1>Welcome to ARGs-OAP Galaxy!</h1>
            <div class="login-info">
                <a v-if="!loginStatus" href="#" @click="onModalShow(1)">Login</a>
                <a v-if="!loginStatus" href="#" @click="onModalShow(2)">Register</a>
                <a v-if="loginStatus" href="#">Welcome, {{ Galaxy.user.attributes.email }}</a>
                <a v-if="loginStatus" href="#" @click="logoutClick">Logout</a>
            </div>
            <img src="/static/args/landing.png" alt="">
        </div>
        <div class="flex">
            <Nav v-show="leftShow" :login="loginStatus" :tab="tab" @change="onChange"/>
            <div v-if="tab === 'home'" class="main-wrap main-wrap-left">
                <AboutInfo/>
                <Tools @result="onChangeTab" :login="loginStatus"/>
                <div class="visitor-status">
                    <h2>Ohter Information</h2>
                    <p>This website is managed by <a href="http://web.hku.hk/~zhangt/ZhangT.htm" target="_blank">The Environmental Biotechnology Laboratory of The University of Hong Kong</a>.</p>
                    <p>Should you have any queries or require further information, please do not hesitate to contact us <a href="mailto:zhangt@hku.hk">here</a>.</p>
                    <h3>Mirror Site</h3>
                    <p>Many users from mainland China have reported experiencing slow upload speed, we have now established an additional <a href="http://smile.sustc.edu.cn/">mirror site</a> in SUSTC (Shenzhen).</p>
                    <h3>Visitor Status</h3>
                    <div><img src="/static/args/visitor-map-2018-11-17.png"/></div>
                </div>
            </div>
            <div v-else-if="tab === 'tool'" class="main-wrap main-wrap-right">
                <Tools @result="onChangeTab" :login="loginStatus"/>
            </div>
            <div v-else-if="tab === 'file'" class="main-wrap main-wrap-right">
                <Files @result="onChangeTab"/>
            </div>
            <div v-else-if="tab === 'result'" class="main-wrap main-wrap-right">
                <Results @result="onChangeTab"/>
            </div>
            <div v-show="rightShow" class="twitter-wrap"><a class="twitter-timeline" data-height="680" href="https://twitter.com/yinxiaole?ref_src=twsrc%5Etfw">Tweets by yinxiaole</a></div>
        </div>
        <b-modal v-model="modalShow" static no-enforce-focus hide-footer>
            <template v-slot:modal-header>
                <h4 v-if="modalMod === 1" class="title" tabindex="0">Login</h4>
                <h4 v-else-if="modalMod === 2" class="title" tabindex="0">Register</h4>
            </template>
            <login v-if="modalMod === 1" :show_welcome_with_login="show_welcome_with_login" :welcome_url="welcome_url"/>
            <register v-else-if="modalMod === 2" :redirect="redirect" :registration_warning_message="registration_warning_message" :mailing_join_addr="mailing_join_addr" :server_mail_configured="server_mail_configured" :terms_url="terms_url"/>
        </b-modal>
    </div>
</template>

<script>
import axios from "axios";
import Nav from './Nav'
import AboutInfo from './AboutInfo'
import Tools from './Tools'
import Files from './Files'
import Results from './Results'

import Login from "./login/Login.vue";
import Register from "./login/Register.vue";
import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
import { getGalaxyInstance } from "app";

Vue.use(BootstrapVue);

export default {
    components: {
        Nav,
        AboutInfo,
        Tools,
        Files,
        Results,
        Login,
        Register
    },
    data() {
        return {
            Galaxy: undefined,
            loginStatus: false,
            tab: 'home',
            leftShow: true,
            rightShow: true,
            modalShow: false,
            modalMod: 0,
            // login
            show_welcome_with_login: false,
            welcome_url: '',
            // register
            redirect: '/args/index',
            registration_warning_message: '',
            mailing_join_addr: '',
            server_mail_configured: '',
            terms_url: ''
        };
    },
    mounted() {
        let recaptchaScript = document.createElement('script')
        recaptchaScript.setAttribute('src', 'https://platform.twitter.com/widgets.js')
        document.head.appendChild(recaptchaScript)
        this.Galaxy = getGalaxyInstance();
        console.log(this.Galaxy)
        if(this.Galaxy.user.id) {
            this.loginStatus = true
        }
        this.onChange(this.tab)
    },
    methods: {
        onModalShow(val) {
            this.modalShow = true
            this.modalMod = val
        },
        onChangeTab(val) {
            console.log('xxxx')
            this.tab = val
            this.onChange(this.tab)
        },
        onChange(val) {
            this.tab = val
            if (val === 'tool') {
                this.rightShow = false
                this.leftShow = true
            } else if (val === 'file') {
                this.rightShow = false
                this.leftShow = true
            } else if (val === 'result') {
                this.rightShow = false
                this.leftShow = true
            } else if (val === 'home') {
                this.rightShow = true
                this.leftShow = false
            } else {
                console.log(val);
            }
        },
        logoutClick() {
            console.log('logout')
            const galaxy = getGalaxyInstance();
            const session_csrf_token = galaxy.session_csrf_token;
            const url = `${galaxy.root}user/logout?session_csrf_token=${session_csrf_token}`;
            axios
                .get(url)
                .then(() => {
                    if (galaxy.user) {
                        galaxy.user.clearSessionStorage();
                    }
                    // Check if we need to logout of OIDC IDP
                    if (galaxy.config.enable_oidc) {
                        return axios.get(`${galaxy.root}authnz/logout`);
                    } else {
                        return {};
                    }
                })
                .then((response) => {
                    window.location = '/args/index'
                });
        }
    }
}
</script>

<style scoped>
body, html {
    padding: 0;
    margin: 0;
}
.header img {
    position: absolute;
    width: 100%;
    z-index: 1;
    top: 0;
    height: 250px;
    left: 0;
    opacity: 0.7;
}
.header .login-info {
    position: absolute;
    z-index: 20;
    top: 20px;
    right: 80px;
}
.header .login-info a {
    color: #eee;
    font-size: 1rem;
    margin: 0 5px;
}
.header h1 {
    font-size: 4rem;
    color: #fff;
    position: relative;
    text-align: center;
    z-index: 10;
    line-height: 250px;
}
.flex {
    display: flex;
    justify-content: space-between;
}
.flex .twitter-wrap {
    width: 25%;
    padding: 40px 20px;
}
.flex .main-wrap {
    width: calc(75% - 200px);
    padding: 40px;
    border-left: 1px solid #ccc;
    border-right: 1px solid #ccc;
}
.flex .main-wrap-left {
    width: calc(75%);
}
.flex .main-wrap-right {
    width: calc(100% - 200px);
}
.flex .main-wrap .visitor-status img {
    width: 100%;
}
</style>