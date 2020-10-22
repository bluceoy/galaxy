<template>
    <div class="tool-wrap">
        <h2>
            Availible Tools
            <span style="float:right;">
            <a v-if="!login" @click="onUploadDialog" style="font-size:1rem;color: #2196F3;cursor: pointer;margin-right:20px;"># Upload</a>
            <a @click="onShowResult" style="font-size:1rem;color: #2196F3;cursor: pointer;"># Result</a>
            </span>
        </h2>
        
        <ul class="collapsible">
            <li>
                <div @click="click(0)" class="collapsible-header">DEMO</div>
                <div class="collapsible-body container-fluid"><DEMO @exec="onExec"/></div>
            </li>
            <li>
                <div @click="click(0)" class="collapsible-header">ARGs-OAP</div>
                <div class="collapsible-body container-fluid"><ARGsOAP @exec="onExec"/></div>
            </li>
            <li>
                <div @click="click(1)" class="collapsible-header">SARGFAM</div>
                <div class="collapsible-body"><SARGFAM @exec="onExec"/></div>
            </li>
        </ul>

        <b-modal v-model="modalShow" static no-enforce-focus hide-footer>
            <template v-slot:modal-header>
                <h4 class="title" tabindex="0">Online Analysis</h4>
            </template>
            <div class="my-tool-wrap"></div>
        </b-modal>
    </div>
</template>

<script>
import $ from "jquery";
import axios from "axios";
import { getGalaxyInstance } from "app";
import ToolForm from "mvc/tool/tool-form";
import DEMO from "./tools/DEMO";
import ARGsOAP from "./tools/ARGsOAP";
import SARGFAM from "./tools/SARGFAM";
export default {
    components: {
        DEMO,
        ARGsOAP,
        SARGFAM
    },
    props: {
        login: {
            type: Boolean,
            default: false,
        }
    },
    data() {
        return {
            modalShow: false
        };
    },
    methods: {
        click(idx) {
            $('.collapsible > li').eq(idx).find('.collapsible-body').toggle(500, 'swing');
        },
        onShowResult() {
            console.log('xxx')
            this.$emit('result', 'result')
        },
        onUploadDialog(e) {
            console.log(e)
            const Galaxy = getGalaxyInstance();
            e.preventDefault();
            Galaxy.upload.show('/');
        },
        onExec(tool, params) {
            const galaxy = getGalaxyInstance();
            const url = `${galaxy.root}api/custom/job`;
            const d = {
                tool_id: tool.id,
                tool_version: tool.version,
                inputs: params
            }
            axios
                .post(url, d)
                .then((response) => {
                    console.log(response)
                });
        }
    }
}
</script>

<style scoped>
.tool-wrap {
    margin-bottom: 40px;
}
.tool-wrap h2 {
    line-height: 40px;
}
.tool-wrap blockquote {
    margin: 20px 0;
    padding-left: 1.5rem;
    border-left: 5px solid #ee6e73;
}
.collapsible {
    padding: 0;
    margin: 0;
    box-shadow: 0 0 30px 10px #eee;
    -webkit-box-shadow: 0 0 30px 10px #eee;
    -moz-box-shadow: 0 0 30px 10px #eee;
}
.collapsible li {
    list-style: none;
    border-bottom: 1px solid #ccc;
}
.collapsible .collapsible-header {
    color: whitesmoke;
    background-color: #5D737E;
    line-height: 60px;
    padding-left: 20px;
    font-size: 16px;
    cursor: pointer;
}
.collapsible .collapsible-body {
    padding: 20px;
    display: none;
}
</style>