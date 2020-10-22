<template>
    <div class="file-wrap">
        <b-breadcrumb>
            <b-breadcrumb-item @click="e => {onChangePos('/')}">Home</b-breadcrumb-item>
            <b-breadcrumb-item v-for="(item, idx) in pos" @click="e => { !item.active ? onChangePos(item.path) : null}" :key="idx" :active="item.active"><span>{{ item.text }}</span></b-breadcrumb-item>
        </b-breadcrumb>

        <b-button @click="onCreateFolderDialog">Create Folder</b-button>
        <b-button @click="onUploadDialog">Upload File(s)</b-button>
        <!-- <b-button @click="onUploadDialog">Upload File(s)</b-button> -->
        
        <b-table :fields="fields" :items="items" :bordered="true">
            <template v-slot:cell(name)="data">
                <b-icon icon="folder" font-scale="1.5" v-if="data.item.type === 'dir'"></b-icon>
                <b-icon icon="document-text" font-scale="1.5" v-else></b-icon>
                <a v-if="data.item.type === 'dir'" href="#" @click="setCurrentPos(currentPos + (currentPos.substr(currentPos.length - 1, 1) === '/' ? '' : '/') + data.value)"><b>{{ data.value }}</b></a>
                <a v-else>{{ data.value }}</a>
            </template>

            <template v-slot:cell(time)="data">
                {{ formatDate(data.item.time * 1000) }}
            </template>

            <template v-slot:cell(action)="data">
                <a href="#" @click="onRemove(data.item.path)">Remove</a>
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

        <b-modal v-model="showUploadDialog" static no-enforce-focus hide-footer>
            <template v-slot:modal-header>
                <h4 class="title" tabindex="0">Upload Files</h4>
            </template>
            <uploader :options="options" class="uploader-example" @file-success="uploadSuccess">
                <uploader-unsupport></uploader-unsupport>
                <uploader-drop>
                    <p>Drop files here to upload or</p>
                    <uploader-btn>select files</uploader-btn>
                    <uploader-btn :directory="true">select folder</uploader-btn>
                </uploader-drop>
                <uploader-list></uploader-list>
            </uploader>
        </b-modal>
    </div>
</template>

<script>
import axios from "axios";
import $ from "jquery";
import Vue from "vue";
import uploader from 'vue-simple-uploader'
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import { getGalaxyInstance } from "app";

Vue.use(uploader);
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);

export default {
    components: {
    },
    data() {
        return {
            options: {
                // https://github.com/simple-uploader/Uploader/tree/develop/samples/Node.js
                target: '/api/upload_v2/',
                testChunks: false,
                processParams: (params) => {
                    params.dir = this.currentPos;
                    console.log(params);
                    return params;
                },
                
            },
            status: "",
            percentage: 0,
            showCreateFolderDialog: false,
            showUploadDialog: false,
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
                            path: (i === 0 ? '/' : this.pos[i - 1].path + '/') + ps[i]
                        })
                    }
                    let idx = this.pos.length
                    if (idx > 0) {
                        this.pos[idx - 1].active = true
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
                            path: f.real_path,
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
            console.log(e);
            this.showUploadDialog = true;
            // const Galaxy = getGalaxyInstance();
            // e.preventDefault();
            // Galaxy.upload.show(this.currentPos);
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
        },
        uploadSuccess(rootFile, file, message, chunk) {
            console.log(rootFile, file, message, chunk);
            this.getCurrentList();
        },
        onRemove(path) {
            const galaxy = getGalaxyInstance();
            axios
                .post(`${galaxy.root}api/file/remove`, { path: path })
                .then((response) => {
                    console.log(response)
                    this.getCurrentList()
                })
                .catch((error) => {
                    const message = error.response.data && error.response.data.err_msg;
                    this.errorMessage = message;
                });
        }
    }
}
</script>

<style scoped>
.file-wrap {
    margin-bottom: 40px;
}
.uploader-example {
    padding: 15px;
    font-size: 12px;
}
.uploader-example .uploader-btn {
    margin-right: 4px;
}
.uploader-example .uploader-list {
    max-height: 440px;
    overflow: auto;
    overflow-x: hidden;
    overflow-y: auto;
}
</style>
