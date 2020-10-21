<template>
    <div class="util-wrap">
        <div class="title">{{ title }}</div>
        <div>
            <b-form-input v-model="value" @input="$emit('parent-event', $event.target.value)"></b-form-input>
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
        };
    },
    methods: {
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
.util-wrap .tip {
    margin: 5px 0;
    font-size: 0.8rem;
}
</style>