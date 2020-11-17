<template>
    <div class="result-wrap">
        <b-table :fields="fields" :items="items" :bordered="true">
            <template v-slot:cell(name)="data">
                <a href="#">{{ data.value }}</a>
            </template>
            <template v-slot:cell(create_time)="data">
                {{ moment(data.value * 1000).format('YYYY/MM/DD HH:mm:ss') }}
            </template>
            <template v-slot:cell(update_time)="data">
                {{ moment(data.value * 1000).format('YYYY/MM/DD HH:mm:ss') }}
            </template>
            <template v-slot:cell(status)="data">
                {{ statusMap[data.value] }}
            </template>
            <template v-slot:cell(action)="data">
                <a href="#" @click="onView(data.item.job_id)">View</a>
            </template>
        </b-table>

        <b-modal v-model="modalShow" static no-enforce-focus hide-footer dialog-class="result-dialog">
            <template v-slot:modal-header>
                <h4 class="title" tabindex="0">Job Detail</h4>
            </template>
            <div class="result-detail">
                <div class="line">
                    <div><span>Job Id:</span> {{ job.job_id }}</div>
                    <div><span>Job Status:</span> {{ statusMap[job.status] }}</div>
                </div>
                <div class="line">
                    <div><span>Tool Id:</span> {{ job.tool_id }}</div>
                    <div><span>Tool Version:</span> {{ job.tool_version }}</div>
                </div>
                <div class="line">
                    <div><span>Tool Name:</span> {{ job.tool_name }}</div>
                    <div><span>Input Params:</span> {{ job.params }}</div>
                </div>
                <div class="line">
                    <div>
                        <p><span>Output File:</span></p>
                        <p v-for="(out, i) in job.output" :key="i"><a href="#" @click="onDownload(out)">{{ out }}</a></p>
                    </div>
                </div>
            </div>
            <div class="result-visualize">
                <h4>Visualize: </h4>
                <div>
                    <div v-if="vData.type === 1">
                        <pre>{{ vData.data }}</pre>
                    </div>
                    <div v-else-if="vData.type === 2">
                        <img :src="vData.url"/>
                    </div>
                </div>
            </div>
        </b-modal>
    </div>
</template>

<script>
import axios from "axios";
import $ from "jquery";
import { getGalaxyInstance } from "app";
import moment from "moment";

export default {
    components: {
    },
    data() {
        return {
            statusMap: {
                1: 'running',
                2: 'done',
                3: 'error'
            },
            outputTypeMap: {
                '__argsoap__': 1,
                '__argsoap2.0__': 1,
                '__argsoap2.2__': 1,
                '__sargfam__': 1,
                '__ivip__': 1,
                '__mst__': 1,
                '__argsosp__': 1,
                '__argpore__': 1
            },
            modalShow: false,
            loginStatus: false,
            fields: [
                { key: 'job_id', label: 'Job Id' },
                { key: 'tool_id', label: 'Tool' },
                { key: 'tool_version', label: 'Version' },
                { key: 'params', label: 'Parmas' },
                { key: 'status', label: 'Status' },
                { key: 'create_time', label: 'Create Time' },
                { key: 'update_time', label: 'Finish Time' },
                'action'
            ],
            items: [],
            job: {},
            vData: {
                type: 1, // 1:txt, 2:pdf, 3:jpg, 4:other
                url: '',
                data: undefined
            },
            pageNo: 1,
            pageSize: 100,
            total: 0
        };
    },
    methods: {
        moment,
        load() {
            const Galaxy = getGalaxyInstance();
            axios
                .get(`${Galaxy.root}api/custom/job/list?page_no=${this.pageNo}&page_size=${this.pageSize}`)
                .then((response) => {
                    this.items = response.data.items
                })
                .catch((error) => {
                    const message = error.response.data && error.response.data.err_msg;
                    this.errorMessage = message;
                });
        },
        onView(id) {
            const Galaxy = getGalaxyInstance();
            axios
                .get(`${Galaxy.root}api/custom/job/detail/${id}`)
                .then((response) => {
                    this.job = response.data
                    this.modalShow = true
                    this.vData.type = this.outputTypeMap[this.job.tool_id]
                    this.vData.url = '',
                    this.vData.data = undefined
                })
                .catch((error) => {
                    const message = error.response.data && error.response.data.err_msg;
                    this.errorMessage = message;
                });
        },
        onDownload(path, save = true) {
            const Galaxy = getGalaxyInstance();
            axios
                .post(`${Galaxy.root}api/file/download`, { path: path }, { responseType: 'blob' })
                .then((response) => {
                    let _that = this
                    if (save) {
                        let s = path.split('/')
                        const link = document.createElement('a')
                        link.href = window.URL.createObjectURL(response.data)
                        link.download = s[s.length - 1]
                        link.click()
                        return
                    }
                    if (this.vData.type === 1) {
                        let reader = new FileReader()
                        reader.onload = function(event) {
                            let content = reader.result
                            _that.vData.data = content
                        }
                        reader.readAsText(response.data)
                    } else if (this.vData.type === 2) {
                        this.vData.url = window.URL.createObjectURL(response.data)
                    }
                })
                .catch((error) => {
                    const message = error.response.data && error.response.data.err_msg;
                    this.errorMessage = message;
                });
        }
    },
    mounted: function() {
        const Galaxy = getGalaxyInstance();
        if(Galaxy.user.id) {
            this.loginStatus = true
        }
        this.load()
    }
}
</script>
<style>
.result-wrap .result-dialog {
    width: 960px;
    max-width: 1200px;
}
</style>
<style scoped>
.result-wrap {
    margin-bottom: 40px;
}
.result-wrap .result-detail .line {
    display: flex;
    justify-content: space-between;
}
.result-wrap .result-detail .line > div {
    width: 50%;
}
.result-wrap .result-detail .line div > span{
    font-weight: bold;
    display: inline-block;
    width: 100px;
}
.result-wrap .result-visualize {
    margin-top: 30px;
    width: 100%;
}
.result-wrap .result-visualize img {
    width: 100%;
}
</style>