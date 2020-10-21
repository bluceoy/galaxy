<template>
    <div class="util-wrap">
        <div class="title">{{ title }}</div>
        <div class="value-wrap">
            <input v-model="value" @input="$emit('parent-event', $event.target.value)" @click="onFocus" readonly/>
            <div v-show="showOption" class="select-wrap">
                <div class="search">
                    <b-input-group>
                        <b-form-input type="text"></b-form-input>
                        <b-input-group-append>
                            <b-input-group-text>
                                <b-icon icon="x" />
                            </b-input-group-text>
                        </b-input-group-append>
                    </b-input-group>
                </div>
                <div>

                </div>
                <div class="foot">
                    <button>Back</button>
                    <button @click="onBlur">Cancel</button>
                </div>
            </div>
        </div>
        <div class="tip">{{ tip }}</div>
    </div>
</template>

<script>
import Vue from "vue";
import BootstrapVue from "bootstrap-vue";
Vue.use(BootstrapVue);
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
        }
    },
    data() {
        return {
            showOption: false
        };
    },
    methods: {
        onFocus() {
            console.log(this.showOption)
            this.showOption = !this.showOption
        },
        onBlur() {
            this.showOption = false
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
    top: 30px;
    left: 0;
    width: 100%;
    max-height: 200px;
    border: 1px solid #ccc;
    background: #fff;
    box-shadow: 0 4px 5px rgba(0, 0, 0, 0.15);
}
.util-wrap input {
    width: 100%;
    padding: 3px;
}
.util-wrap .tip {
    margin: 5px 0;
    font-size: 0.8rem;
}
</style>