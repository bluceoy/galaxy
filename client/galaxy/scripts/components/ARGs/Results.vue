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
                <!-- <a @click="onView(data.item.job_id)">View</a>
                |
                <a>Rerun</a>
                |
                <a @click="onDownload(data.item.output)">Download</a> -->
            </template>
        </b-table>

        <b-modal v-model="modalShow" static no-enforce-focus hide-footer size="lg">
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
                    <div><span>Output File:</span> {{ job.output }}</div>
                </div>
            </div>
            <div class="result-visualize">
                <h4>Visualize: </h4>
                <div>
                    
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
            modalShow: false,
            loginStatus: false,
            fields: [
                { key: 'job_id', label: 'Job Id' },
                { key: 'tool_id', label: 'Tool' },
                { key: 'tool_version', label: 'Version' },
                { key: 'params', label: 'Parmas' },
                { key: 'output', label: 'Output' },
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
                data: {}
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
                    // 获取结果，如果支持可视化，则进行渲染
                    this.onDownload(this.job.output)
                    this.modalShow = true
                })
                .catch((error) => {
                    const message = error.response.data && error.response.data.err_msg;
                    this.errorMessage = message;
                });
        },
        onDownload(path) {
            const Galaxy = getGalaxyInstance();
            axios
                .post(`${Galaxy.root}api/file/download`, { path: path })
                .then((response) => {
                    this.vData.data = response.data
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
</style>