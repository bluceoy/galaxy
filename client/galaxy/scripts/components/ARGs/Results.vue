<template>
    <div class="file-wrap">
        <b-table :fields="fields" :items="items" :bordered="true">
            <template v-slot:cell(name)="data">
                <a href="#">{{ data.value }}</a>
            </template>
            <template v-slot:cell(create_time)="data">
                {{ moment.utc(data.value).format() }}
            </template>
            <template v-slot:cell(action)="data">
                <a @click="onView(data.item.job_id)">View</a>
                |
                <a>Rerun</a>
                |
                <a>Download</a>
            </template>
        </b-table>
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
            loginStatus: false,
            fields: [
                { key: 'job_id', label: 'Job Id' },
                { key: 'tool', label: 'Tool' },
                { key: 'version', label: 'Version' },
                { key: 'state', label: 'State' },
                { key: 'create_time', label: 'Create Time' },
                { key: 'finish_time', label: 'Finish Time' },
                'action'
            ],
            items: [],
            job: {},
            pageNo: 1,
            pageSize: 100,
            total: 0
        };
    },
    methods: {
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
            if(Galaxy.user.id) {
                this.loginStatus = true
            }
            axios
                .get(`${Galaxy.root}api/custom/job/detail/${id}`)
                .then((response) => {
                    this.job = response.data.items
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
.file-wrap {
    margin-bottom: 40px;
}
</style>