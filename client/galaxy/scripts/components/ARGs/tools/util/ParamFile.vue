<template>
    <div class="util-wrap">
        <div class="title">{{ title }}</div>
        <div class="value-wrap">
            <b-form-input v-model="inputValue" @input="$emit('parent-event', $event.target.value)" @click="onFocus" readonly></b-form-input>
            <div v-show="showOption" class="select-wrap">
                <div class="head">
                    <b-input-group>
                        <b-form-input v-model="searching" placeholder="Type to Search"></b-form-input>
                        <b-input-group-append>
                            <b-input-group-text>
                                <b-icon icon="x" @click="onClearSearch"/>
                            </b-input-group-text>
                        </b-input-group-append>
                    </b-input-group>
                </div>
                <div class="main">
                    <ul>
                        <li v-for="(item, idx) in items" :key="idx" @click="onSelect(item, idx)">
                            <b-icon icon="folder" font-scale="1.2" v-if="item.type === 'dir'"></b-icon>
                            <b-icon icon="document-text" font-scale="1.2" v-else></b-icon>
                            {{ item.name }}
                        </li>
                    </ul>
                </div>
                <div class="foot">
                    <div class="back">
                        <b-button @click="onBack" :disabled="currentPos === '/'">
                            <b-icon icon="arrow-left"></b-icon> Back
                        </b-button>
                        {{ currentPos }}
                    </div>
                    <button @click="onChoose" v-show="folder">Choose Current Folder</button>
                    <button @click="onBlur">Cancel</button>
                </div>
            </div>
        </div>
        <div class="tip">{{ tip }}</div>
    </div>
</template>

<script>
import axios from "axios";
import Vue from "vue";
import { getGalaxyInstance } from "app";
import { connectableObservableDescriptor } from 'rxjs/internal/observable/ConnectableObservable';
export default {
    model: {
      prop: 'value',
      event: 'parent-event'
    },
    props: {
        value: {
            type: String,
            default: '',
        },
        title: {
            type: String,
            default: '',
        },
        tip: {
            type: String,
            default: '',
        },
        folder: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            inputValue: '',
            showOption: false,
            searching: '',
            items: [],
            currentPos: '',
            pos: []
        };
    },
    created() {
        const Galaxy = getGalaxyInstance();
        this.getCurrentPos()
    },
    methods: {
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
        onBack() {
            console.log(this.pos)
            let ps = this.currentPos.split('/').filter(e => { return e !== '' })
            if (ps.length > 0) {
                let dir = (ps.slice(0, ps.length - 1)).join('/')
                this.setCurrentPos('/' + dir)
            }
        },
        onSelect(item, idx) {
            console.log(item)
            if (item.type === 'dir') {
                this.setCurrentPos(this.currentPos + (this.currentPos.substr(this.currentPos.length - 1, 1) === '/' ? '' : '/') + item.name)
            } else {
                if (!this.folder) {
                    this.inputValue = item.path
                    this.onBlur()
                }
            }
        },
        onChoose() {
            this.inputValue = this.currentPos
            this.onBlur()
        },
        onFocus() {
            console.log(this.showOption)
            this.showOption = !this.showOption
        },
        onBlur() {
            this.showOption = false
        },
        onClearSearch() {
            this.searching = '';
        }
    }
}
</script>

<style scoped>
.util-wrap {
    margin-bottom: 10px;
}
.util-wrap .title {
    font-size: 1rem;
    font-weight: bold;
    margin: 5px 0;
}
.util-wrap .value-wrap {
    position: relative;
}
.util-wrap .select-wrap {
    position: absolute;
    top: 34px;
    left: 0;
    width: 100%;
    padding: 10px;
    min-height: 120px;
    border: 1px solid #ccc;
    background: #fff;
    box-shadow: 0 4px 5px rgba(0, 0, 0, 0.15);
}
.util-wrap .select-wrap .main {
    width: 100%;
    min-height: 50px;
    max-height: 200px;
    margin: 10px 0;
    overflow: auto;
}
.util-wrap .select-wrap .main ul {
    list-style: none;
    padding: 0;
    margin: 0;
}
.util-wrap .select-wrap .main li {
    list-style: none;
    padding: 0 5px;
    margin: 0;
    font-size: 0.9rem;
    line-height: 28px;
}
.util-wrap .select-wrap .main li:hover {
    background: #ccc;
}
.util-wrap .select-wrap .foot {
    border-top: 1px solid #ccc;
    width: 100%;
    padding-top: 10px;
    text-align: right;
}
.util-wrap .select-wrap .foot .back {
    float: left;
}
.util-wrap .tip {
    margin: 5px 0;
    font-size: 0.8rem;
}
</style>