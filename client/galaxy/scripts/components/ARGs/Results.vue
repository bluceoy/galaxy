<template>
    <div class="file-wrap">

        <b-table :fields="fields" :items="items" :bordered="true">
            <template v-slot:cell(name)="data">
                <b class="text-info">{{ data.value }}</b>
            </template>
            <template v-slot:cell(action)="data">
                <i>View</i>
                <i>Edit</i>
                <i>Remove</i>
            </template>
        </b-table>
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
            fields: [
                { key: 'dataset_id', label: 'Dataset Id' },
                { key: 'name', label: 'Name' },
                { key: 'state', label: 'State' },
                { key: 'create_time', label: 'Create Time' },
                'action'
            ],
            items: [],
        };
    },
    methods: {
        load() {
            const Galaxy = getGalaxyInstance();
            if(Galaxy.user.id) {
                this.loginStatus = true
            }

            console.log(Galaxy);
            this.items = [];
            Galaxy.currHistoryPanel.model.contents.models.forEach(e => {
                this.items.push(e.attributes)
            });
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