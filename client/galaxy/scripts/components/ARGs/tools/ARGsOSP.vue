<template>
    <div>
        <h3>ARGs-OSP: Antibiotic Resistant Genes Online Searching Platform</h3>
        
        <blockquote>
            ARGs-OSP is online search platfrom that provides a global ARG profile covering the information of their phylogenetic and ecological distribution. Search and download functionality are designed for users to retrieve the occurrence of ARGs in different taxonomy and the abundance of ARGs in different habitats. Through data sharing, ARGs-OSP aims to motivate and facilitate future studies into mining new information and knowledge from the combined data, without making repeated efforts in dataset processing.
        </blockquote>

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

        <p><a target="_blank" href="https://args-osp.herokuapp.com/">ARGs-OSP v1.0 (External Link)</a></p>
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
                id: '__argsosp__',
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
