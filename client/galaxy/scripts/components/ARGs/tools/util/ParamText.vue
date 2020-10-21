<template>
    <div class="util-wrap">
        <div class="title">{{ title }}</div>
        <div><input v-model="value" @input="$emit('parent-event', $event.target.value)" /></div>
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
.util-wrap input {
    width: 100%;
    padding: 3px;
}
.util-wrap .tip {
    margin: 5px 0;
    font-size: 0.8rem;
}
</style>