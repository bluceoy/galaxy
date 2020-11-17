<template>
    <div class="donemessagelarge"><!-- 执行成功提示内容 -->
        <p>Executed <b>{{ name }}</b> and successfully added 1 job to the queue.</p>
        <p>The tool uses this input:</p>
        <p class="messagerow" v-for="(e, i) in input" :key="i">
            <b>{{ e }}</b>
        </p>
        <p>It produces 2 outputs:</p>
        <p class="messagerow" v-for="(e, i) in output" :key="i">
            <b>{{ e }}</b>
        </p>
        <p>You can check the status of queued jobs and view the resulting data by refreshing the History panel. When the job has been run the status will change from 'running' to 'finished' if completed successfully or 'error' if problems were encountered.</p>
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
            default: '',
        },
        input: {
            type: Array,
            default: () => { return [] }
        },
        output: {
            type: Array,
            default: () => { return [] }
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