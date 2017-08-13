
package us.kbase.kbgoexpress;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: GOExpressInput</p>
 * <pre>
 * required params:
 * workspace_name: Name of the workspace
 * expressionset_ref: ExpressionSet object reference
 * condition1: First condition 
 * condition2: Second condition
 * Number of permutations: num_permutations
 *     optional params:
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "expression_ref",
    "genome_ref",
    "sample_id1",
    "sample_n_conditions",
    "num_permutations",
    "fold_change_cutoff"
})
public class GOExpressInput {

    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("expression_ref")
    private java.lang.String expressionRef;
    @JsonProperty("genome_ref")
    private java.lang.String genomeRef;
    @JsonProperty("sample_id1")
    private List<String> sampleId1;
    @JsonProperty("sample_n_conditions")
    private List<Map<String, String>> sampleNConditions;
    @JsonProperty("num_permutations")
    private Long numPermutations;
    @JsonProperty("fold_change_cutoff")
    private Double foldChangeCutoff;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public GOExpressInput withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("expression_ref")
    public java.lang.String getExpressionRef() {
        return expressionRef;
    }

    @JsonProperty("expression_ref")
    public void setExpressionRef(java.lang.String expressionRef) {
        this.expressionRef = expressionRef;
    }

    public GOExpressInput withExpressionRef(java.lang.String expressionRef) {
        this.expressionRef = expressionRef;
        return this;
    }

    @JsonProperty("genome_ref")
    public java.lang.String getGenomeRef() {
        return genomeRef;
    }

    @JsonProperty("genome_ref")
    public void setGenomeRef(java.lang.String genomeRef) {
        this.genomeRef = genomeRef;
    }

    public GOExpressInput withGenomeRef(java.lang.String genomeRef) {
        this.genomeRef = genomeRef;
        return this;
    }

    @JsonProperty("sample_id1")
    public List<String> getSampleId1() {
        return sampleId1;
    }

    @JsonProperty("sample_id1")
    public void setSampleId1(List<String> sampleId1) {
        this.sampleId1 = sampleId1;
    }

    public GOExpressInput withSampleId1(List<String> sampleId1) {
        this.sampleId1 = sampleId1;
        return this;
    }

    @JsonProperty("sample_n_conditions")
    public List<Map<String, String>> getSampleNConditions() {
        return sampleNConditions;
    }

    @JsonProperty("sample_n_conditions")
    public void setSampleNConditions(List<Map<String, String>> sampleNConditions) {
        this.sampleNConditions = sampleNConditions;
    }

    public GOExpressInput withSampleNConditions(List<Map<String, String>> sampleNConditions) {
        this.sampleNConditions = sampleNConditions;
        return this;
    }

    @JsonProperty("num_permutations")
    public Long getNumPermutations() {
        return numPermutations;
    }

    @JsonProperty("num_permutations")
    public void setNumPermutations(Long numPermutations) {
        this.numPermutations = numPermutations;
    }

    public GOExpressInput withNumPermutations(Long numPermutations) {
        this.numPermutations = numPermutations;
        return this;
    }

    @JsonProperty("fold_change_cutoff")
    public Double getFoldChangeCutoff() {
        return foldChangeCutoff;
    }

    @JsonProperty("fold_change_cutoff")
    public void setFoldChangeCutoff(Double foldChangeCutoff) {
        this.foldChangeCutoff = foldChangeCutoff;
    }

    public GOExpressInput withFoldChangeCutoff(Double foldChangeCutoff) {
        this.foldChangeCutoff = foldChangeCutoff;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((((((("GOExpressInput"+" [workspaceName=")+ workspaceName)+", expressionRef=")+ expressionRef)+", genomeRef=")+ genomeRef)+", sampleId1=")+ sampleId1)+", sampleNConditions=")+ sampleNConditions)+", numPermutations=")+ numPermutations)+", foldChangeCutoff=")+ foldChangeCutoff)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
