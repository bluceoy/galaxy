<template>
    <div class="util-wrap">
        <div class="title">{{ title }}</div>
        <div>
            <b-form-input v-model="inputValue"></b-form-input>
        </div>
        <div class="tip">{{ tip }}</div>
    </div>
</template>

<script>
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
            inputValue: '',
        };
    },
    watch: {
        inputValue: function() {
            this.$emit('parent-event', this.inputValue);
        }
    },
    created() {
        this.inputValue = this.value
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