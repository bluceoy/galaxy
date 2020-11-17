<template>
    <div>
        <h3>SARGFAM</h3>
        
        <blockquote>
            Sargfam database and profile Hidden Markov Models based alignment algorithm for ARGs-like sequences annotation were a function module in ARGs-OAP v2.0, supporting supplementary sequence retrieval strategy to current similarity search method (i.e. UBLAST and BLAST), especially applied on detecting remote homolog (novel genes).
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

        <p><a href="#" @click="showHowToUse = true">How to use</a><a v-if="showHowToUse" @click="showHowToUse = false" href="#" style="margin-left:20px;">Collapse</a></p>
        <div v-show="showHowToUse" class="info-wrap">
            <p>To conduct HMMSCAN against Sargfam, users should locally assemble raw reads into contigs first and predict ORFs within the contigs, and then those predicted ORFs (in fasta format) can be uploaded to the online Galaxy for identification of ARG-like protein. The results summarized in table listed the exact ARG types and subtypes the input sequences were annotated can be downloaded from the online server. Currently the pipeline only accept proteins sequences as input query but we are working on this and in the near future new services will be supplemented for nucleotide sequences. HMMER 3 suite (hmmer.org/) is the fundamental tool to do the above mentioned alignment. Indeed, we use HMMSCAN input sequences against Sargfam with parameter ¨-cut_ga, which stands for inclusive optimized cut off gathering threshold (GA).</p>
        </div>

        <p><a href="#" @click="showUnderTheHood = true">Under The Hood</a><a v-if="showUnderTheHood" @click="showUnderTheHood = false" href="#" style="margin-left:20px;">Collapse</a></p>
        <div v-show="showUnderTheHood" class="info-wrap">
            <p>From 12307 ARGs sequences within the comprehensive SARG v2.0 database, 9080 sequences belonged to 189 ARGs subtypes, each of which contains more than 3 sequences, were selected as candidates for profile HMMs of ARGs¡¯ construction. For each subtype, maximum-likelihood phylogenetic tree was constructed and those questionable sequence(s) which was distantly related to the core cluster were filtered out. Then, train subset was randomly chosen from each subtype and used for profile HMMs constructed by HMMER 3 suite, while the remaining sequences were used as the test subset for validation. After that, a specific gathering threshold (GA) was selected in the range of 1 to 3000 for each profile HMM to optimize the quality for the constructed model by Shell scripts. Lastly, the validation was conducted for each profile HMM by retrieving target sequences through HMMSCAN from a specific test mixture of target sequences with non-target sequences in other subtypes to calculate the recall and precision value. Those profile HMMs with both precision and recall values over 80% were retained as the validated profiles. Sargfam was the gathering of these profiles and formatted models for ARGs annotation.</p>
        </div>

        <p><a href="#" @click="showHowToCite = true">How To Cite</a><a v-if="showHowToCite" @click="showHowToCite = false" href="#" style="margin-left:20px;">Collapse</a></p>
        <div v-show="showHowToCite" class="info-wrap">
            <blockquote>
                Yin, X, X-T Jiang, B. Chai, L. Li, Y. Yang, J. R. Cole, J. M. Tiedje*, and T. Zhang*.(2018) "ARGs-OAP v2. 0 with an Expanded SARG Database and Hidden Markov Models for Enhancement Characterization and Quantification of Antibiotic Resistance Genes in Environmental Metagenomes." Bioinformatics 1:8. DOI:10.1093/bioinformatics/bty053.
            </blockquote>
        </div>

        <p><a href="#" @click="showContacts = true">Contacts</a><a v-if="showContacts" @click="showContacts = false" href="#" style="margin-left:20px;">Collapse</a></p>
        <div v-show="showContacts" class="info-wrap">
            <p>LiGuan Li: leeliguan@gmail.com</p>
            <p>Xiaole Yin: yinlele99@gmail.com</p>
        </div>
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
            showHowToUse: false,
            showUnderTheHood: false,
            showHowToCite: false,
            showContacts: false,
            tool: {
                id: '__sargfam__',
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
