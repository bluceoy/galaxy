<template>
    <div>
        <h3>I-VIP: Integron Visualization and Identification Pipeline</h3>
        
        <blockquote>
            The Integron Visualization and Identification Pipeline (I-VIP) is a well-organized pipeline to identify, classify, annotate and visualize class 1 integrons (Fig 1) in complete/draft genomes and assembled metagenomes. To facilitate flexible application by the users, I-VIP was separated into two modules; Module A for integron identification and classification (orange framework in Fig 1), and Module B for integron extraction, annotation and visualization (blue framework in Fig 1). The I-VIP also provides multiple optional parameters and diverse output formats for further analysis by the user end.
        </blockquote>

        <div>
            <img src="/static/args/tools/Figure3.png" style="width:600px">
            <p>Fig. 1. Flow chart of I-VIP</p>
        </div>

        <p><a @click="showOnlineAnalysis = true" href="#">Online Analysis</a><a v-if="showOnlineAnalysis" @click="showOnlineAnalysis = false" href="#" style="margin-left:20px;">Collapse</a></p>
        <div v-show="showOnlineAnalysis">
            <div v-if="mode === 1" class="my-tool-wrap">
                <!-- params -->
                <ParamFile v-model="params.input1" title="Source Fasta File" tip=""></ParamFile>
                <!-- operation -->
                <b-button variant="primary" @click="onExecute">
                    <b-icon icon="check"></b-icon> Execute
                </b-button>
            </div>
            <div v-else-if="mode === 2" class="donemessagelarge"><!-- 执行成功提示内容 -->
                <p>Executed <b>Microbial source tracking</b> and successfully added 1 job to the queue.</p>
                <p>The tool uses this input:</p>
                <p class="messagerow">
                    <b>{{ params.input1 }}</b>
                </p>
                <p>It produces 2 outputs:</p>
                <p class="messagerow">
                    <b>Standard deviation of source proportions after running 5 times</b>
                </p>
                <p class="messagerow">
                    <b>Average of source proportions after running 5 times</b>
                </p>
                <p>You can check the status of queued jobs and view the resulting data by refreshing the History panel. When the job has been run the status will change from 'running' to 'finished' if completed successfully or 'error' if problems were encountered.</p>
            </div>
            <div v-else-if="mode === 3"><!-- 执行失败提示内容 -->
            </div>
        </div>

        <p><a target="_blank" href="https://github.com/caozhichongchong/I-VIP/blob/master/I-VIP%20User%20Manual.pdf">Manual</a></p>
        <p><a target="_blank" href="https://github.com/caozhichongchong/I-VIP/archive/master.zip">Download</a></p>
        <p><a target="_blank" href="https://github.com/caozhichongchong/I-VIP">Repository</a></p>
    </div>
</template>

<script>
import * as U from './util/index.js'
export default {
    components: {
	    ParamText: U.ParamText,
        ParamFile: U.ParamFile,
        ParamSelect: U.ParamSelect
  	},
    data() {
        return {
            mode: 1, // 1表单，2成功提示，3失败提示
            showOnlineAnalysis: false,
            tool: {
                id: '__ivip__',
                version: '1.0.0'
            },
            params: {
                input1: ''
            }
        };
    },
    methods: {
        onExecute() {
            this.$emit('exec', this.tool, this.params, (res) => {
                this.mode = 2
            });
        }
    }
}
</script>

<style scoped src="./util/index.css"></style>
