<template>
    <div>
        <h3>ARGs-OSP: Antibiotic Resistant Genes Online Searching Platform</h3>
        
        <blockquote>
            ARGs-OSP is online search platfrom that provides a global ARG profile covering the information of their phylogenetic and ecological distribution. Search and download functionality are designed for users to retrieve the occurrence of ARGs in different taxonomy and the abundance of ARGs in different habitats. Through data sharing, ARGs-OSP aims to motivate and facilitate future studies into mining new information and knowledge from the combined data, without making repeated efforts in dataset processing.
        </blockquote>

        <p><a @click="showOnlineAnalysis = true" href="#">Online Analysis</a><a v-if="showOnlineAnalysis" @click="showOnlineAnalysis = false" href="#" style="margin-left:20px;">Collapse</a></p>
        <div v-show="showOnlineAnalysis" class="my-tool-wrap">
            <!-- params -->
            <ParamFile v-model="params.input1" title="Source Fasta File" tip=""></ParamFile>
            <!-- operation -->
            <b-button variant="primary" @click="onExecute">
                <b-icon icon="check"></b-icon> Execute
            </b-button>
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
            showOnlineAnalysis: false,
            tool: {
                id: '__args_index__',
                version: '1.0.0'
            },
            params: {
                input1: ''
            }
        };
    },
    methods: {
        onExecute() {
            this.$emit('exec', this.tool, this.params);
        }
    }
}
</script>

<style scoped>
blockquote {
    border-left: 5px solid #ee6e73;
    padding-left: 20px;
    margin: 20px 0;
}
.my-tool-wrap {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 15px;
    margin: 15px 0;
}
.info-wrap {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 15px;
    margin: 15px 0;
}
</style>