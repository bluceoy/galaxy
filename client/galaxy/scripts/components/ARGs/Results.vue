<template>
    <div class="file-wrap">

        <!-- <b-table :fields="fields" :items="items" :bordered="true">
            <template v-slot:cell(job_name)="data">
                <b class="text-info">{{ data.value }}</b>
            </template>
            <template v-slot:cell(action)="data">
                <i>View</i>
                <i>Edit</i>
                <i>Remove</i>
            </template>
        </b-table>
        <b-pagination-nav v-model="pageNo" :number-of-pages="pageTotal"></b-pagination-nav> -->
        <template v-if="loginStatus">
            <div class="history" v-show="showMode === 1"></div>
            <div v-show="showMode === 2"><b-button @click="load">Back</b-button></div>
            <div class="one-history" v-show="showMode === 2"></div>
        </template>
        <template v-else>
            <div class="current-history"></div>
        </template>
    </div>
</template>

<script>
import $ from "jquery";
import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
import { getGalaxyInstance } from "app";
import HistoryList from "./history/history-list";
import HistoryView from "components/HistoryView.vue";

Vue.use(BootstrapVue);

export default {
    components: {
    },
    data() {
        return {
            loginStatus: false,
            showMode: 1, // 1集合2列表3详细
            pageNo: 1,
            pageSize: 10,
            pageTotal: 1,
            fields: [
                { key: 'job_no', label: 'Job No.' },
                { key: 'job_name', label: 'Job Name' },
                { key: 'time', label: 'Time' },
                { key: 'status', label: 'Status' },
                'action'
            ],
            items: [
                { job_no: 40, job_name: 'work-001', time: 0, status: 1 },
                { job_no: 21, job_name: 'work-002', time: 0, status: 2 },
                { job_no: 89, job_name: 'work-003', time: 0, status: 2 },
                { job_no: 89, job_name: 'work-004', time: 0, status: 2 },
                { job_no: 39, job_name: 'work-005', time: 0, status: 2 }
            ],
        };
    },
    methods: {
        load() {
            const Galaxy = getGalaxyInstance();
            if(Galaxy.user.id) {
                this.loginStatus = true
            }
            if (this.loginStatus) {
                this.$nextTick(() => {
                    const view = new HistoryList.View({ action_id: 'list', select_callback: this.onSelect });
                    $(".history")
                        .empty()
                        .scrollTop(0)
                        .append(view.$el || view)
                        .show();
                    Galaxy.trigger("center-panel:load", view);
                    this.showMode = 1
                })
            } else {
                this.$nextTick(() => {
                    $(".current-history")
                        .empty()
                        .scrollTop(0)
                        .append(Galaxy.currHistoryPanel.$el)
                        .show();
                })
            }
        },
        onSelect(id) {
            const Galaxy = getGalaxyInstance();
            const historyInstance = Vue.extend(HistoryView);
            const vm = document.createElement("div");
            $(".one-history")
                .empty()
                .scrollTop(0)
                .append(vm.$el || vm)
                .show();
            Galaxy.trigger("center-panel:load", vm);
            new historyInstance({ propsData: { id: id } }).$mount(vm);
            this.showMode = 2;
        }
    },
    mounted: function() {
        this.load()
    }
}
</script>

<style scoped>
.file-wrap {
    margin-bottom: 40px;
}
</style>