<template>
    <div>
        <h3>ARGPORE</h3>
        
        <blockquote>
            This tool can help users to identify ARG hits on nanopore reads and simultaneously find the carrier population of the identified ARGs by searching against phylogenetic marker genes on nanopore reads.
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
            <SuccessTip v-else-if="mode === 2" :name="tool.id" :input="[params.input1]" :output="['HMMSCAN-SARGFAM']"></SuccessTip>
            <FailTip v-else-if="mode === 3" :name="tool.id" :msg="'some thing wrong'"></FailTip>
        </div>

        <p><a href="#" @click="showHowToUse = true">How to use</a><a v-if="showHowToUse" @click="showHowToUse = false" href="#" style="margin-left:20px;">Collapse</a></p>
        <div v-show="showHowToUse" class="info-wrap">
            <p>ARGpore is designed to predict resistome of 2D.fasta/1D.fasta generated from NanoPore sequencing.</p>

            <p>NOTE: If you have metagenomic-assembled contig/scaffold, we suggest you to use the ARG-host pipeline which combines the ARGpore taxa algorithm and taxa voting algorithm. You may still use ARGpore for your metagenomic-assembled contig/scaffold, but you would lose a lot of ARGs and taxa due to annotation limitation.</p>

            <p>Input file:</p>
            <p>Input of ARGpore is simply your 2D.fasta/1D.fasta</p>
            <ul>
                <li>
                    Resistome prediction Algorithm:
                    <ol>
                        <li>Your input fasta will be searched against nt-version SARG database (v1.0)</li>
                        <li>Valid alignment with > 80% similarity over > 70% alignment length will be kept for further filtering of overlap regions</li>
                        <li>If two hit regions on the same read overlaped for > 50% alignment length,only the one with longest ARG hit will be kept</li>
                    </ol>
                </li>
                <li>
                    Taxa Algorithm:
                    <ol>
                        <li>Your input fasta will be searched against clade specific marker gene database (MetaPhlan 2)</li>
                        <li>Valid alignment with > 80% similarity over > 70% alignment length will be kept for taxa annotation</li>
                        <li>Only the best hit with highest bitscore is kept to determine phylogenetic affiliation</li>
                    </ol>
                </li>
            </ul>
            <p>A table with sample names as column name, and ARG sequence/gene name as row name (this is the default format of output table in ARG sequence/gene level after running ARGs-OAP)</p>

            <p>Output files:</p>
            <ul>
                <li>taxa.tab: nanopore reads with valid match to clade specific marker gene</li>
                <li>arg.tab: nanopore reads with valid match to SARG database</li>
                <li>arg.w.taxa.tab: ARG-containing nanopore reads with taxa annotated</li>
                <li>arg.species.summary.tab: ARG-containing nanopore reads counting by ARG-type</li>
            </ul>
        </div>

        <p><a href="#" @click="showHowToCite = true">How To Cite</a><a v-if="showHowToCite" @click="showHowToCite = false" href="#" style="margin-left:20px;">Collapse</a></p>
        <div v-show="showHowToCite" class="info-wrap">
            <blockquote>
                Xia, Yu, An-Dong Li, Yu Deng, Xiao-Tao Jiang, Li-Guan Li, and Tong Zhang. MinION Nanopore Sequencing Enables Correlation between Resistome Phenotype and Genotype of Coliform Bacteria in Municipal Sewage. Frontiers in Microbiology 2017
            </blockquote>
        </div>
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
            showHowToUse: false,
            showHowToCite: false,
            tool: {
                id: '__argpore__',
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
