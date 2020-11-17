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
            <SuccessTip v-else-if="mode === 2" :name="tool.id" :input="params.input1" :output="['HMMSCAN-SARGFAM']"></SuccessTip>
            <FailTip v-else-if="mode === 3" :name="tool.id" :msg="'some thing wrong'"></FailTip>
        </div>

        <p><a target="_blank" href="https://args-osp.herokuapp.com/">ARGs-OSP v1.0 (External Link)</a></p>
    </div>
</template>

<script>
import * as U from './util/index.js'
export default {
    components: {
        SuccessTip: U.SuccessTip,
        FailTip: U.FailTip,
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
    created() {
        this.mode = 1
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
