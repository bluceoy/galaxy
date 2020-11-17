<template>
    <div class="donemessagelarge"><!-- 执行失败提示内容 -->
        <p>Executed <b>{{ name }}</b> and fail.</p>
        <p>The error message:</p>
        <p class="messagerow">
            <b>{{ msg }}</b>
        </p>
    </div>
</template>

<script>
export default {
    model: {
      prop: 'value',
      event: 'parent-event'
    },
    props: {
        name: {
            type: String,
            default: ''
        },
        msg: {
            type: String,
            default: ''
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