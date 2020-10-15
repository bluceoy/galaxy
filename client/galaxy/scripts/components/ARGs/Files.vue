<template>
    <div class="file-wrap">
        <b-breadcrumb>
            <b-breadcrumb-item @click="e => {onChangePos('/')}">Home</b-breadcrumb-item>
            <b-breadcrumb-item v-for="(item, idx) in pos" @click="e => { !item.active ? onChangePos(item.path) : null}" :key="idx" :active="item.active"><span>{{ item.text }}</span></b-breadcrumb-item>
        </b-breadcrumb>
        
        <b-button @click="onCreateFolderDialog">Create Folder</b-button>
        <b-button @click="onUploadDialog">Upload File(s)</b-button>

        <b-table :fields="fields" :items="items" :bordered="true">
            <template v-slot:cell(name)="data">
                <b-icon icon="folder" font-scale="1.5" v-if="data.item.type === 'dir'"></b-icon>
                <a class="text-info" v-if="data.item.type === 'dir'" href="#" @click="setCurrentPos(currentPos + (currentPos.lastIndexOf('/') > -1 ? '' : '/') + data.value)">{{ data.value }}</a>
                <a class="text-info" v-else>{{ data.value }}</a>
            </template>

            <template v-slot:cell(time)="data">
                {{ formatDate(data.item.time * 1000) }}
            </template>

            <template v-slot:cell(action)="data">
                <i>View</i>
                <i>Edit</i>
                <i>Remove</i>
            </template>
        </b-table>

        <b-modal v-model="showCreateFolderDialog" static no-enforce-focus hide-footer>
            <template v-slot:modal-header>
                <h4 class="title" tabindex="0">Create New Folder</h4>
            </template>
            <b-form @submit="onSubmitCreateFolder">
                <b-form-group id="input-group" label="New Folder Name:" label-for="input">
                    <b-form-input id="input" v-model="newFolderName" required placeholder="Enter folder name"></b-form-input>
                </b-form-group>
                <b-button type="submit" variant="primary">Submit</b-button>
            </b-form>
        </b-modal>
    </div>
</template>

<script>
import axios from "axios";
import $ from "jquery";
import Vue from "vue";
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import { getGalaxyInstance } from "app";

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

export default {
    components: {
    },
    data() {
        return {
            status: "",
            percentage: 0,
            showCreateFolderDialog: false,
            // 当前位置
            currentPos: '',
            pos: [],
            // 新建文件夹
            newFolderName: '',
            // 文件列表
            pageNo: 1,
            pageSize: 10,
            pageTotal: 1,
            fields: [
                { key: 'name', label: 'Name' },
                { key: 'type', label: 'Type' },
                { key: 'size', label: 'Size' },
                { key: 'time', label: 'Time' },
                { key: 'status', label: 'Status' },
                'action'
            ],
            items: []
        };
    },
    created() {
        const Galaxy = getGalaxyInstance();

        Galaxy.upload.model.on("change", () => {
            this.status = Galaxy.upload.model.attributes.status;
            this.percentage = Galaxy.upload.model.attributes.percentage;
        });

        this.getCurrentPos()
    },
    methods: {
        formatDate(ts) {
            let d = new Date(ts)
            return d.toLocaleString()
        },
        onChangePos(e) {
            console.log(e)
            this.setCurrentPos(e)
        },
        getCurrentPos() {
            const galaxy = getGalaxyInstance();
            const url = `${galaxy.root}api/file/getdir`;
            axios
                .get(url)
                .then((response) => {
                    console.log(response)
                    this.currentPos = response.data.current_dir
                    let ps = this.currentPos.split('/').filter(e => { return e !== '' })
                    console.log(ps)
                    this.pos = []
                    for (let i = 0; i < ps.length; i ++) {
                        this.pos.push({
                            text: ps[i],
                            path: (i === 0 ? '/' : this.pos[i - 1].path) + ps[i].text
                        })
                    }
                    let idx = this.pos.length - 1
                    if (idx >= 0) {
                        this.pos[idx].active = true
                    }
                    this.getCurrentList()
                });
        },
        setCurrentPos(dir) {
            // 进入某个目录
            const galaxy = getGalaxyInstance();
            axios
                .post(`${galaxy.root}api/file/setdir`, { path: dir })
                .then((response) => {
                    console.log(response)
                    this.getCurrentPos()
                })
                .catch((error) => {
                    const message = error.response.data && error.response.data.err_msg;
                    this.errorMessage = message;
                });
        },
        getCurrentList() {
            const galaxy = getGalaxyInstance();
            const url = `${galaxy.root}api/file/list`;
            axios
                .get(url)
                .then((response) => {
                    console.log(response)
                    this.items = []
                    response.data.files.forEach((f, i) => {
                        this.items.push({
                            id: i + 1,
                            name: f.file,
                            type: f.type,
                            size: f.size,
                            time: f.ctime,
                            status: 0
                        })
                    });
                });
        },
        createFolder() {
            const galaxy = getGalaxyInstance();
            axios
                .post(`${galaxy.root}api/file/addfolder`, { path: this.currentPos + (this.currentPos.substr(this.currentPos.length - 1, 1) === '/' ? '' : '/') + this.newFolderName })
                .then((response) => {
                    console.log(response)
                    this.getCurrentList()
                })
                .catch((error) => {
                    const message = error.response.data && error.response.data.err_msg;
                    this.errorMessage = message;
                });
        },
        onUploadDialog(e) {
            console.log(e)
            const Galaxy = getGalaxyInstance();
            e.preventDefault();
            Galaxy.upload.show(this.currentPos);
        },
        onCreateFolderDialog(e) {
            console.log(e);
            this.showCreateFolderDialog = true
        },
        onSubmitCreateFolder(e) {
            e.preventDefault()
            console.log(this.newFolderName)
            this.createFolder()
            this.showCreateFolderDialog = false
        }
    }
}
</script>

<style scoped>
.file-wrap {
    margin-bottom: 40px;
}
</style>