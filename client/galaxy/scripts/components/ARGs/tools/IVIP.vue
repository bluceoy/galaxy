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
        <div v-show="showOnlineAnalysis" class="my-tool-wrap">
            <!-- params -->
            <ParamFile v-model="params.input1" title="Source Fasta File" tip=""></ParamFile>
            <!-- operation -->
            <b-button variant="primary" @click="onExecute">
                <b-icon icon="check"></b-icon> Execute
            </b-button>
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