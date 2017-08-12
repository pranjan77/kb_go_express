
package us.kbase.kbgoexpress;

import java.util.HashMap;
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
    "expressionset_ref",
    "condition_label",
    "num_permutations",
    "fold_change_cutoff"
})
public class GOExpressInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("expressionset_ref")
    private String expressionsetRef;
    @JsonProperty("condition_label")
    private String conditionLabel;
    @JsonProperty("num_permutations")
    private Long numPermutations;
    @JsonProperty("fold_change_cutoff")
    private Double foldChangeCutoff;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public GOExpressInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("expressionset_ref")
    public String getExpressionsetRef() {
        return expressionsetRef;
    }

    @JsonProperty("expressionset_ref")
    public void setExpressionsetRef(String expressionsetRef) {
        this.expressionsetRef = expressionsetRef;
    }

    public GOExpressInput withExpressionsetRef(String expressionsetRef) {
        this.expressionsetRef = expressionsetRef;
        return this;
    }

    @JsonProperty("condition_label")
    public String getConditionLabel() {
        return conditionLabel;
    }

    @JsonProperty("condition_label")
    public void setConditionLabel(String conditionLabel) {
        this.conditionLabel = conditionLabel;
    }

    public GOExpressInput withConditionLabel(String conditionLabel) {
        this.conditionLabel = conditionLabel;
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
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((("GOExpressInput"+" [workspaceName=")+ workspaceName)+", expressionsetRef=")+ expressionsetRef)+", conditionLabel=")+ conditionLabel)+", numPermutations=")+ numPermutations)+", foldChangeCutoff=")+ foldChangeCutoff)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
