<template>
  <div class="preview-container">
    <header class="preview-header">
      <div class="preview-header-content">
        <NuxtLink to="/" class="back-link">← Mission Control</NuxtLink>
        <h1>{{ journeyName || journeyKey }}</h1>
        <p class="journey-meta">{{ journeyKey }} · Version {{ journeyVersion }} · KYCP Components</p>
      </div>
    </header>

    <div v-if="error" class="error-message">
      <strong>Failed to load schema.</strong>
      <p>{{ error }}</p>
    </div>
    
    <div v-else-if="!loading" class="preview-content">
      <div class="form-container">
        <!-- Tools -->
        <div class="tools">
          <label><input type="checkbox" v-model="debugExplain" /> Explain visibility</label>
        </div>
        <!-- Error Summary -->
        <div v-if="Object.keys(errors).length > 0" class="error-summary">
          <h3>Please correct the following errors:</h3>
          <ul>
            <li v-for="(error, key) in errors" :key="key">
              {{ error }}
            </li>
          </ul>
        </div>
        
        <!-- Accordion layout for future journeys -->
        <KycpAccordion
          v-if="useAccordionLayout"
          :sections="accordionSections"
          expand-first
        >
          <template
            v-for="(accordion, index) in accordionSections"
            #[`section-${index}`]="{ section }"
          >
            <div class="accordion-section">
              <div
                v-if="fieldsForAccordion(section.key).length === 0 && groupsForAccordion(section.key).length === 0"
                class="accordion-empty"
              >
                <p class="accordion-empty__title">No questions to show yet</p>
                <p class="accordion-empty__hint">Complete the previous sections or adjust your answers to reveal what's next.</p>
              </div>

              <!-- Special handling for sections with visual field grouping -->
              <template v-if="hasFieldGrouping(section.key)">
                <div v-for="group in getFieldGroupsForSection(section.key)" :key="group.title" class="field-group">
                  <div class="field-group-header">
                    <h4 class="field-group-title">{{ group.title }}</h4>
                  </div>
                  <div class="field-group-content">
                    <div v-for="field in group.fields" :key="field.key" class="field-container" :class="getFieldHierarchyClass(field)">
                      <!-- Same field rendering logic as below but with hierarchy classes -->
                      <!-- Statement fields -->
                      <KycpStatement 
                        v-if="field.style === 'statement'"
                        :text="displayLabel(field)"
                      />
                      
                      <!-- Divider/Title fields -->
                      <KycpDivider 
                        v-else-if="field.style === 'divider'"
                        :title="displayLabel(field)"
                      />
                      
                      <!-- Regular form fields -->
                      <KycpFieldWrapper 
                        v-else
                        :id="field.key"
                        :label="displayLabel(field)"
                        :required="field.validation?.required"
                        :description="field.description"
                        :error="errors[field.key]"
                        :help="displayHelp(field)"
                      >
                        <!-- Field input components (same as below) -->
                        <KycpInput
                          v-if="field.type === 'string' || field.type === 'text'"
                          :id="field.key"
                          v-model="formData[field.key]"
                          :placeholder="field.placeholder"
                          :required="field.validation?.required"
                          :maxlength="field.validation?.maxLength || 1024"
                          :error="!!errors[field.key]"
                        />
                        
                        <KycpTextarea
                          v-else-if="field.type === 'freeText' || field.type === 'textarea'"
                          :id="field.key"
                          v-model="formData[field.key]"
                          :placeholder="field.placeholder"
                          :required="field.validation?.required"
                          :maxlength="field.validation?.maxLength || 8192"
                          :rows="4"
                          :error="!!errors[field.key]"
                        />
                        
                        <KycpInput
                          v-else-if="field.type === 'integer'"
                          :id="field.key"
                          v-model.number="formData[field.key]"
                          type="number"
                          :placeholder="field.placeholder"
                          :required="field.validation?.required"
                          :min="field.validation?.min || 0"
                          :max="field.validation?.max || 2147483647"
                          :step="1"
                          :error="!!errors[field.key]"
                        />
                        
                        <KycpInput
                          v-else-if="field.type === 'decimal'"
                          :id="field.key"
                          v-model.number="formData[field.key]"
                          type="number"
                          :placeholder="field.placeholder"
                          :required="field.validation?.required"
                          :step="0.01"
                          :error="!!errors[field.key]"
                        />
                        
                        <KycpInput
                          v-else-if="field.type === 'date'"
                          :id="field.key"
                          v-model="formData[field.key]"
                          type="date"
                          :placeholder="field.placeholder || 'DD/MM/YYYY'"
                          :required="field.validation?.required"
                          :error="!!errors[field.key]"
                        />
                        
                        <KycpSelect
                          v-else-if="field.type === 'lookup' || field.type === 'enum'"
                          :id="field.key"
                          v-model="formData[field.key]"
                          :options="field.options || []"
                          :placeholder="field.placeholder || 'Please select...'"
                          :required="field.validation?.required"
                          :error="!!errors[field.key]"
                        />
                        
                        <KycpInput
                          v-else
                          :id="field.key"
                          v-model="formData[field.key]"
                          :placeholder="field.placeholder"
                          :required="field.validation?.required"
                          :error="!!errors[field.key]"
                        />
                      </KycpFieldWrapper>

                      <!-- Debug: explain visibility for field -->
                      <div v-if="debugExplain" class="debug-explain">
                        <div class="debug-field-info">
                          <span class="debug-label">Field:</span> 
                          <code class="debug-field-key">{{ field.key }}</code>
                        </div>
                        
                        <template v-if="hasCopyChange(field)">
                          <div class="debug-copy">
                            <div class="debug-title">Copy changes</div>
                            <p class="debug-row"><span class="debug-label">Original (AS-IS):</span> {{ copyOriginal(field)?.label }}</p>
                            <p v-if="copyOriginal(field)?.help" class="debug-row muted">{{ copyOriginal(field)?.help }}</p>
                            <p v-if="copyFuture(field)?.label" class="debug-row"><span class="debug-label">Proposed:</span> {{ copyFuture(field)?.label }}</p>
                            <p v-if="copyFuture(field)?.help" class="debug-row muted">{{ copyFuture(field)?.help }}</p>
                            <p class="debug-meta" v-if="copyFuture(field)?.source || copyFuture(field)?.rationale">
                              <span class="debug-label">Source:</span> {{ copyFuture(field)?.source || 'Unspecified' }}
                              <span v-if="copyFuture(field)?.rationale" class="muted">— {{ copyFuture(field)?.rationale }}</span>
                            </p>
                          </div>
                        </template>
                        <template v-else>
                          <p class="muted">No copy changes recorded.</p>
                        </template>

                        <template v-if="(field.visibility && field.visibility.length)">
                          <div class="debug-title">Visibility rules:</div>
                          <ul>
                            <li v-for="(cond, idx) in conditionsForField(field)" :key="idx">
                              <span :class="{'pass': cond.pass, 'fail': !cond.pass}">•</span>
                              {{ cond.sourceKey }} {{ cond.operator }} {{ cond.value }}
                              <span class="muted">(current: {{ cond.current }})</span>
                            </li>
                          </ul>
                        </template>
                        <template v-else>
                          <div class="muted">No visibility rules</div>
                        </template>
                      </div>
                    </div>
                  </div>
                </div>
              </template>

              <!-- Standard field rendering for all other sections -->
              <div v-else v-for="field in fieldsForAccordion(section.key)" :key="field.key" class="field-container">
                <!-- Statement fields -->
                <KycpStatement 
                  v-if="field.style === 'statement'"
                  :text="displayLabel(field)"
                />
                
                <!-- Divider/Title fields -->
                <KycpDivider 
                  v-else-if="field.style === 'divider'"
                  :title="displayLabel(field)"
                />
                
                <!-- Regular form fields -->
                <KycpFieldWrapper 
                  v-else
                  :id="field.key"
                  :label="displayLabel(field)"
                  :required="field.validation?.required"
                  :description="field.description"
                  :error="errors[field.key]"
                  :help="displayHelp(field)"
                >
                  <!-- String/Text input -->
                  <KycpInput
                    v-if="field.type === 'string' || field.type === 'text'"
                    :id="field.key"
                    v-model="formData[field.key]"
                    :placeholder="field.placeholder"
                    :required="field.validation?.required"
                    :maxlength="field.validation?.maxLength || 1024"
                    :error="!!errors[field.key]"
                  />
                  
                  <!-- FreeText/Textarea -->
                  <KycpTextarea
                    v-else-if="field.type === 'freeText' || field.type === 'textarea'"
                    :id="field.key"
                    v-model="formData[field.key]"
                    :placeholder="field.placeholder"
                    :required="field.validation?.required"
                    :maxlength="field.validation?.maxLength || 8192"
                    :rows="4"
                    :error="!!errors[field.key]"
                  />
                  
                  <!-- Integer -->
                  <KycpInput
                    v-else-if="field.type === 'integer'"
                    :id="field.key"
                    v-model.number="formData[field.key]"
                    type="number"
                    :placeholder="field.placeholder"
                    :required="field.validation?.required"
                    :min="field.validation?.min || 0"
                    :max="field.validation?.max || 2147483647"
                    :step="1"
                    :error="!!errors[field.key]"
                  />
                  
                  <!-- Decimal -->
                  <KycpInput
                    v-else-if="field.type === 'decimal'"
                    :id="field.key"
                    v-model.number="formData[field.key]"
                    type="number"
                    :placeholder="field.placeholder"
                    :required="field.validation?.required"
                    :step="0.01"
                    :error="!!errors[field.key]"
                  />
                  
                  <!-- Date -->
                  <KycpInput
                    v-else-if="field.type === 'date'"
                    :id="field.key"
                    v-model="formData[field.key]"
                    type="date"
                    :placeholder="field.placeholder || 'DD/MM/YYYY'"
                    :required="field.validation?.required"
                    :error="!!errors[field.key]"
                  />
                  
                  <!-- Lookup/Select -->
                  <KycpSelect
                    v-else-if="field.type === 'lookup' || field.type === 'enum'"
                    :id="field.key"
                    v-model="formData[field.key]"
                    :options="field.options || []"
                    :placeholder="field.placeholder || 'Please select...'"
                    :required="field.validation?.required"
                    :error="!!errors[field.key]"
                  />
                  
                  <!-- Fallback for unknown types -->
                  <KycpInput
                    v-else
                    :id="field.key"
                    v-model="formData[field.key]"
                    :placeholder="field.placeholder"
                    :required="field.validation?.required"
                    :error="!!errors[field.key]"
                  />
                </KycpFieldWrapper>

                <!-- Debug: explain visibility for the field -->
                <div v-if="debugExplain" class="debug-explain">
                  <div class="debug-field-info">
                    <span class="debug-label">Field:</span> 
                    <code class="debug-field-key">{{ field.key }}</code>
                  </div>
                  
                  <div v-if="hasCopyChange(field)" class="debug-copy">
                    <div class="debug-title">Copy changes</div>
                    <p class="debug-row"><span class="debug-label">Original (AS-IS):</span> {{ copyOriginal(field)?.label }}</p>
                    <p v-if="copyOriginal(field)?.help" class="debug-row muted">{{ copyOriginal(field)?.help }}</p>
                    <p v-if="copyFuture(field)?.label" class="debug-row"><span class="debug-label">Proposed:</span> {{ copyFuture(field)?.label }}</p>
                    <p v-if="copyFuture(field)?.help" class="debug-row muted">{{ copyFuture(field)?.help }}</p>
                    <p class="debug-meta" v-if="copyFuture(field)?.source || copyFuture(field)?.rationale">
                      <span class="debug-label">Source:</span> {{ copyFuture(field)?.source || 'Unspecified' }}
                      <span v-if="copyFuture(field)?.rationale" class="muted">— {{ copyFuture(field)?.rationale }}</span>
                    </p>
                  </div>
                  <template v-else>
                    <p class="muted">No copy changes recorded.</p>
                  </template>

                  <template v-if="optionChanges(field).length">
                    <div class="debug-title">Lookup updates</div>
                    <ul>
                      <li v-for="(opt, idx) in optionChanges(field)" :key="idx">
                        <span class="debug-label">Original:</span> {{ opt.original }}
                        <br />
                        <span class="debug-label">Proposed:</span> {{ opt.updated }}
                      </li>
                    </ul>
                  </template>

                  <template v-if="(field.visibility && field.visibility.length)">
                    <div class="debug-title">Visibility rules</div>
                    <ul>
                      <li v-for="(cond, idx) in conditionsForField(field)" :key="idx">
                        <span :class="{'pass': cond.pass, 'fail': !cond.pass}">•</span>
                        {{ cond.sourceKey }} {{ cond.operator }} {{ cond.value }}
                        <span class="muted">(current: {{ cond.current }})</span>
                      </li>
                    </ul>
                  </template>
                  <template v-else>
                    <div class="muted">No visibility rules.</div>
                  </template>
                </div>
              </div>

              <!-- Complex Groups (repeaters) -->
              <div v-for="grp in groupsForAccordion(section.key)" :key="grp.key" class="group-container">
                <KycpDivider :title="grp.label || grp.key" />
                <KycpRepeater v-model="formData[grp.key]" :item-label="grp.label || grp.key" :title-field="grp.titleField">
                  <template #item="{ item }">
                    <div style="font-size: 13px; color: var(--kycp-gray-700);">
                      {{ grp.titleField && item[grp.titleField] ? item[grp.titleField] : 'Row' }}
                    </div>
                  </template>
                  <template #form="{ item, save, cancel }">
                    <div style="display: grid; gap: 16px;">
                      <div v-for="child in groupChildFields(grp)" :key="child.key" v-show="evaluateVisibilityForModel(child, item)">
                        <KycpFieldWrapper :id="child.key" :label="displayLabel(child)" :required="child.validation?.required" :description="child.description" :help="displayHelp(child)">
                          <KycpInput
                            v-if="child.type === 'string' || child.type === 'text'"
                            :id="child.key"
                            v-model="item[child.key]"
                            :maxlength="child.validation?.maxLength || 1024"
                          />
                          <KycpTextarea
                            v-else-if="child.type === 'freeText' || child.type === 'textarea'"
                            :id="child.key"
                            v-model="item[child.key]"
                            :maxlength="child.validation?.maxLength || 8192"
                            :rows="4"
                          />
                          <KycpInput
                            v-else-if="child.type === 'integer'"
                            :id="child.key"
                            v-model.number="item[child.key]"
                            type="number"
                            :min="child.validation?.min || 0"
                            :max="child.validation?.max || 2147483647"
                            :step="1"
                          />
                          <KycpInput
                            v-else-if="child.type === 'decimal'"
                            :id="child.key"
                            v-model.number="item[child.key]"
                            type="number"
                            :step="0.01"
                          />
                          <KycpInput
                            v-else-if="child.type === 'date'"
                            :id="child.key"
                            v-model="item[child.key]"
                            type="date"
                            :placeholder="child.placeholder || 'DD/MM/YYYY'"
                          />
                          <KycpSelect
                            v-else-if="child.type === 'lookup' || child.type === 'enum'"
                            :id="child.key"
                            v-model="item[child.key]"
                            :options="child.options || []"
                            :placeholder="child.placeholder || 'Please select...'"
                          />
                          <KycpInput
                            v-else
                            :id="child.key"
                            v-model="item[child.key]"
                          />
                        </KycpFieldWrapper>

                        <!-- Debug: explain visibility for group child field -->
                        <div v-if="debugExplain" class="debug-explain">
                          <div class="debug-field-info">
                            <span class="debug-label">Field:</span> 
                            <code class="debug-field-key">{{ child.key }}</code>
                          </div>
                          
                          <div v-if="hasCopyChange(child)" class="debug-copy">
                            <div class="debug-title">Copy changes</div>
                            <p class="debug-row"><span class="debug-label">Original (AS-IS):</span> {{ copyOriginal(child)?.label }}</p>
                            <p v-if="copyOriginal(child)?.help" class="debug-row muted">{{ copyOriginal(child)?.help }}</p>
                            <p v-if="copyFuture(child)?.label" class="debug-row"><span class="debug-label">Proposed:</span> {{ copyFuture(child)?.label }}</p>
                            <p v-if="copyFuture(child)?.help" class="debug-row muted">{{ copyFuture(child)?.help }}</p>
                            <p class="debug-meta" v-if="copyFuture(child)?.source || copyFuture(child)?.rationale">
                              <span class="debug-label">Source:</span> {{ copyFuture(child)?.source || 'Unspecified' }}
                              <span v-if="copyFuture(child)?.rationale" class="muted">— {{ copyFuture(child)?.rationale }}</span>
                            </p>
                          </div>
                          <template v-else>
                            <p class="muted">No copy changes recorded.</p>
                          </template>

                          <template v-if="(child.visibility && child.visibility.length)">
                            <div class="debug-title">Visibility rules</div>
                            <ul>
                              <li v-for="(cond, idx) in conditionsForField(child, item)" :key="idx">
                                <span :class="{'pass': cond.pass, 'fail': !cond.pass}">•</span>
                                {{ cond.sourceKey }} {{ cond.operator }} {{ cond.value }}
                                <span class="muted">(current: {{ cond.current }})</span>
                              </li>
                            </ul>
                          </template>
                          <template v-else>
                            <div class="muted">No visibility rules.</div>
                          </template>
                        </div>
                      </div>
                      <div style="display: flex; gap: 12px; justify-content: flex-end;">
                        <KycpButton variant="secondary" label="Cancel" @trigger="cancel" />
                        <KycpButton variant="primary" label="Save" @trigger="save" />
                      </div>
                    </div>
                  </template>
                </KycpRepeater>
              </div>
            </div>
          </template>
        </KycpAccordion>

        <!-- Fallback legacy layout -->
        <template v-else>
          <div v-for="section in sections" :key="section" class="form-section">
            <KycpDivider v-if="section !== 'General'" :title="section" />
            
            <div v-for="field in fieldsBySection(section)" :key="field.key" class="field-container">
            <!-- Statement fields -->
            <KycpStatement 
              v-if="field.style === 'statement'"
              :text="displayLabel(field)"
            />
            
            <!-- Divider/Title fields -->
            <KycpDivider 
              v-else-if="field.style === 'divider'"
              :title="displayLabel(field)"
            />
            
            <!-- Regular form fields -->
            <KycpFieldWrapper 
              v-else
              :id="field.key"
              :label="displayLabel(field)"
              :required="field.validation?.required"
              :description="field.description"
              :error="errors[field.key]"
              :help="displayHelp(field)"
            >
              <!-- String/Text input -->
              <KycpInput
                v-if="field.type === 'string' || field.type === 'text'"
                :id="field.key"
                v-model="formData[field.key]"
                :placeholder="field.placeholder"
                :required="field.validation?.required"
                :maxlength="field.validation?.maxLength || 1024"
                :error="!!errors[field.key]"
              />
              
              <!-- FreeText/Textarea -->
              <KycpTextarea
                v-else-if="field.type === 'freeText' || field.type === 'textarea'"
                :id="field.key"
                v-model="formData[field.key]"
                :placeholder="field.placeholder"
                :required="field.validation?.required"
                :maxlength="field.validation?.maxLength || 8192"
                :rows="4"
                :error="!!errors[field.key]"
              />
              
              <!-- Integer -->
              <KycpInput
                v-else-if="field.type === 'integer'"
                :id="field.key"
                v-model.number="formData[field.key]"
                type="number"
                :placeholder="field.placeholder"
                :required="field.validation?.required"
                :min="field.validation?.min || 0"
                :max="field.validation?.max || 2147483647"
                :step="1"
                :error="!!errors[field.key]"
              />
              
              <!-- Decimal -->
              <KycpInput
                v-else-if="field.type === 'decimal'"
                :id="field.key"
                v-model.number="formData[field.key]"
                type="number"
                :placeholder="field.placeholder"
                :required="field.validation?.required"
                :step="0.01"
                :error="!!errors[field.key]"
              />
              
              <!-- Date -->
              <KycpInput
                v-else-if="field.type === 'date'"
                :id="field.key"
                v-model="formData[field.key]"
                type="date"
                :placeholder="field.placeholder || 'DD/MM/YYYY'"
                :required="field.validation?.required"
                :error="!!errors[field.key]"
              />
              
              <!-- Lookup/Select -->
              <KycpSelect
                v-else-if="field.type === 'lookup' || field.type === 'enum'"
                :id="field.key"
                v-model="formData[field.key]"
                :options="field.options || []"
                :placeholder="field.placeholder || 'Please select...'"
                :required="field.validation?.required"
                :error="!!errors[field.key]"
              />
              
              <!-- Fallback for unknown types -->
              <KycpInput
                v-else
                :id="field.key"
                v-model="formData[field.key]"
                :placeholder="field.placeholder"
                :required="field.validation?.required"
                :error="!!errors[field.key]"
              />
            </KycpFieldWrapper>

            <!-- Debug: explain visibility for the field -->
            <div v-if="debugExplain" class="debug-explain">
              <div class="debug-field-info">
                <span class="debug-label">Field:</span> 
                <code class="debug-field-key">{{ field.key }}</code>
              </div>
              
              <template v-if="(field.visibility && field.visibility.length)">
                <div class="debug-title">Visibility rules:</div>
                <ul>
                  <li v-for="(cond, idx) in conditionsForField(field)" :key="idx">
                    <span :class="{'pass': cond.pass, 'fail': !cond.pass}">•</span>
                    {{ cond.sourceKey }} {{ cond.operator }} {{ cond.value }}
                    <span class="muted">(current: {{ cond.current }})</span>
                  </li>
                </ul>
              </template>
              <template v-else>
                <div class="muted">No visibility rules</div>
              </template>
            </div>
          </div>

            <!-- Complex Groups (repeaters) for this section -->
            <div v-for="grp in groupsForSection(section)" :key="grp.key" class="group-container">
            <KycpDivider :title="grp.label || grp.key" />
            <KycpRepeater v-model="formData[grp.key]" :item-label="grp.label || grp.key" :title-field="grp.titleField">
              <template #item="{ item }">
                <div style="font-size: 13px; color: var(--kycp-gray-700);">
                  {{ grp.titleField && item[grp.titleField] ? item[grp.titleField] : 'Row' }}
                </div>
              </template>
              <template #form="{ item, save, cancel }">
                <div style="display: grid; gap: 16px;">
                  <div v-for="child in groupChildFields(grp)" :key="child.key" v-show="evaluateVisibilityForModel(child, item)">
                    <KycpFieldWrapper :id="child.key" :label="displayLabel(child)" :required="child.validation?.required" :description="child.description" :help="displayHelp(child)">
                      <KycpInput
                        v-if="child.type === 'string' || child.type === 'text'"
                        :id="child.key"
                        v-model="item[child.key]"
                        :maxlength="child.validation?.maxLength || 1024"
                      />
                      <KycpTextarea
                        v-else-if="child.type === 'freeText' || child.type === 'textarea'"
                        :id="child.key"
                        v-model="item[child.key]"
                        :maxlength="child.validation?.maxLength || 8192"
                        :rows="4"
                      />
                      <KycpInput
                        v-else-if="child.type === 'integer'"
                        :id="child.key"
                        v-model.number="item[child.key]"
                        type="number"
                        :min="child.validation?.min || 0"
                        :max="child.validation?.max || 2147483647"
                        :step="1"
                      />
                      <KycpInput
                        v-else-if="child.type === 'decimal'"
                        :id="child.key"
                        v-model.number="item[child.key]"
                        type="number"
                        :step="0.01"
                      />
                      <KycpInput
                        v-else-if="child.type === 'date'"
                        :id="child.key"
                        v-model="item[child.key]"
                        type="date"
                        :placeholder="child.placeholder || 'DD/MM/YYYY'"
                      />
                      <KycpSelect
                        v-else-if="child.type === 'lookup' || child.type === 'enum'"
                        :id="child.key"
                        v-model="item[child.key]"
                        :options="child.options || []"
                        :placeholder="child.placeholder || 'Please select...'"
                      />
                      <KycpInput
                        v-else
                        :id="child.key"
                        v-model="item[child.key]"
                      />
                    </KycpFieldWrapper>

                    <!-- Debug: explain visibility for group child field -->
                    <div v-if="debugExplain" class="debug-explain">
                      <div class="debug-field-info">
                        <span class="debug-label">Field:</span> 
                        <code class="debug-field-key">{{ child.key }}</code>
                      </div>
                      
                      <div v-if="hasCopyChange(child)" class="debug-copy">
                        <div class="debug-title">Copy changes</div>
                        <p class="debug-row"><span class="debug-label">Original (AS-IS):</span> {{ copyOriginal(child)?.label }}</p>
                        <p v-if="copyOriginal(child)?.help" class="debug-row muted">{{ copyOriginal(child)?.help }}</p>
                        <p v-if="copyFuture(child)?.label" class="debug-row"><span class="debug-label">Proposed:</span> {{ copyFuture(child)?.label }}</p>
                        <p v-if="copyFuture(child)?.help" class="debug-row muted">{{ copyFuture(child)?.help }}</p>
                        <p class="debug-meta" v-if="copyFuture(child)?.source || copyFuture(child)?.rationale">
                          <span class="debug-label">Source:</span> {{ copyFuture(child)?.source || 'Unspecified' }}
                          <span v-if="copyFuture(child)?.rationale" class="muted">— {{ copyFuture(child)?.rationale }}</span>
                        </p>
                      </div>
                      <template v-else>
                        <p class="muted">No copy changes recorded.</p>
                      </template>

                      <template v-if="optionChanges(child).length">
                        <div class="debug-title">Lookup updates</div>
                        <ul>
                          <li v-for="(opt, idx) in optionChanges(child)" :key="idx">
                            <span class="debug-label">Original:</span> {{ opt.original }}
                            <br />
                            <span class="debug-label">Proposed:</span> {{ opt.updated }}
                          </li>
                        </ul>
                      </template>

                      <template v-if="(child.visibility && child.visibility.length)">
                        <div class="debug-title">Visibility rules</div>
                        <ul>
                          <li v-for="(cond, idx) in conditionsForField(child, item)" :key="idx">
                            <span :class="{'pass': cond.pass, 'fail': !cond.pass}">•</span>
                            {{ cond.sourceKey }} {{ cond.operator }} {{ cond.value }}
                            <span class="muted">(current: {{ cond.current }})</span>
                          </li>
                        </ul>
                      </template>
                      <template v-else>
                        <div class="muted">No visibility rules.</div>
                      </template>
                    </div>
                  </div>
                  <div style="display: flex; gap: 12px; justify-content: flex-end;">
                    <KycpButton variant="secondary" label="Cancel" @trigger="cancel" />
                    <KycpButton variant="primary" label="Save" @trigger="save" />
                  </div>
                </div>
              </template>
            </KycpRepeater>
            </div>
          </div>
        </template>
        
        <!-- Submit button only -->
        <div class="form-actions">
          <KycpButton 
            variant="primary"
            label="Submit"
            @trigger="submitForm"
          />
        </div>
      </div>
    </div>
    
    <!-- Floating Tools: Explain visibility toggle -->
    <div class="floating-tools">
      <label><input type="checkbox" v-model="debugExplain" /> Explain visibility</label>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from 'vue'
import KycpInput from '~/components/kycp/base/KycpInput.vue'
import KycpTextarea from '~/components/kycp/base/KycpTextarea.vue'
import KycpSelect from '~/components/kycp/base/KycpSelect.vue'
import KycpFieldWrapper from '~/components/kycp/base/KycpFieldWrapper.vue'
import KycpStatement from '~/components/kycp/base/KycpStatement.vue'
import KycpDivider from '~/components/kycp/base/KycpDivider.vue'
import KycpButton from '~/components/kycp/base/KycpButton.vue'
import KycpRepeater from '~/components/kycp/base/KycpRepeater.vue'
import KycpAccordion from '~/components/kycp/base/KycpAccordion.vue'

const route = useRoute()
const journeyKey = computed(() => route.params.journey as string)

// Load schema
const { data: schema, error: schemaError, pending: loading } = await useFetch(`/api/schema/${journeyKey.value}`)

const error = computed(() => {
  if (schemaError.value) return 'Failed to load journey schema'
  if (!schema.value) return 'No schema found'
  return null
})

// Extract journey metadata
const journeyName = computed(() => schema.value?.name || '')
const journeyVersion = computed(() => schema.value?.version || '1.0.0')

// Form data
const formData = reactive<Record<string, any>>({})
const errors = reactive<Record<string, string>>({})
const debugExplain = ref(false)
onMounted(() => {
  const q: any = route.query || {}
  if (q && (q.debug !== undefined || q.explain !== undefined)) {
    const v = (q.debug ?? q.explain ?? '').toString().toLowerCase()
    debugExplain.value = v === '1' || v === 'true' || v === '' // presence enables
  }
})

// Fields processing
const allFields = computed(() => {
  if (!schema.value?.fields) return []
  // Filter out internal fields
  return schema.value.fields.filter((f: any) => !f.internal && !f.internal_only)
})

// Groups metadata and helpers
// Prefer explicit complex fields in schema over legacy groups metadata
const complexFields = computed(() => allFields.value.filter((f: any) => f.type === 'complex'))
const groups = computed(() => {
  if (complexFields.value.length) {
    return complexFields.value.map((cf: any) => ({
      key: cf.key,
      children: cf.children || [],
      titleField: cf.titleField || null,
      label: cf.label || cf.key
    }))
  }
  return (schema.value?.groups || []) as any[]
})
const fieldMap = computed(() => {
  const m: Record<string, any> = {}
  for (const f of allFields.value) m[f.key] = f
  return m
})
const groupedChildKeys = computed(() => new Set((groups.value || []).flatMap((g: any) => g.children || [])))
// Exclude grouped children and complex parent fields from main listing
const displayFields = computed(() => allFields.value.filter((f: any) => !groupedChildKeys.value.has(f.key) && f.type !== 'complex'))

function slugify(value: string): string {
  return (value || '')
    .toString()
    .normalize('NFKD')
    .replace(/[&]/g, ' and ')
    .replace(/[’'`]/g, '')
    .replace(/[–—]/g, '-')
    .replace(/[^a-zA-Z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .toLowerCase() || 'legacy-content'
}

const rawAccordionConfig = computed(() => {
  const config = schema.value?.accordions
  if (!config || !Array.isArray(config)) return [] as any[]
  return config as any[]
})

const accordionSections = computed(() => {
  if (!rawAccordionConfig.value.length) return [] as Array<{ key: string; id: string; title: string; description?: string; order: number; expanded?: boolean }>
  const mapped = rawAccordionConfig.value.map((item: any, idx: number) => {
    const key = item.key || slugify(item.title || `section-${idx + 1}`)
    return {
      key,
      id: item.id || key,
      title: item.title || item.name || key.replace(/-/g, ' '),
      description: item.description || '',
      order: item.order ?? idx,
      expanded: item.expanded || false
    }
  })
  
  // Only add legacy-content accordion if there are actually fields that would be assigned to it
  const hasLegacy = mapped.some(section => section.key === 'legacy-content')
  if (!hasLegacy) {
    // Check if any fields would be assigned to legacy-content
    const mappedKeys = new Set(mapped.map(section => section.key))
    const hasOrphanedFields = visibleFields.value.some((field: any) => {
      if (!field) return true
      if (field.accordionKey) return !mappedKeys.has(field.accordionKey)
      const rawSection = typeof field._section === 'string' ? field._section : ''
      const slug = rawSection ? slugify(rawSection) : 'legacy-content'
      return slug === 'legacy-content' || !mappedKeys.has(slug)
    })
    
    if (hasOrphanedFields) {
      mapped.push({ key: 'legacy-content', id: 'legacy-content', title: 'Additional Questions', order: 999 })
    }
  }
  return mapped.sort((a, b) => (a.order ?? 0) - (b.order ?? 0))
})

const accordionKeySet = computed(() => new Set(accordionSections.value.map(section => section.key)))
const useAccordionLayout = computed(() => accordionSections.value.length > 0)

function accordionKeyForField(field: any): string {
  if (!field) return 'legacy-content'
  if (field.accordionKey) return field.accordionKey
  const rawSection = typeof field._section === 'string' ? field._section : ''
  const slug = rawSection ? slugify(rawSection) : 'legacy-content'
  return accordionKeySet.value.has(slug) ? slug : 'legacy-content'
}

function fieldsForAccordion(accordionKey: string) {
  return visibleFields.value.filter((field: any) => accordionKeyForField(field) === accordionKey)
}

// Generalized Field Grouping System
const FIELD_GROUPING_CONFIG = {
  'b2-pre-application-assessment': {
    groups: [
      { title: 'Pre-Application Setup', pattern: /^GENIndicativeAppetiteQuestions$/ },
      { title: 'Entity Structure', pattern: /^GENIndicativeAppetite.*(3rdParty|Admin|Country)/ },
      { title: 'Controlling Parties', pattern: /^GENIndicativeAppetite.*(Fund|OpeningInvestment)/ },
      { title: 'Investment Profile', pattern: /^GENIndicativeAppetite.*(Investment|Risk|highrisk)/ },
      { title: 'Product Requirements', pattern: /^GENIndicativeAppetite.*Product/ },
      { title: 'PEPs & Compliance', pattern: /^GENIndicativeAppetite.*(PEP|SWF|Membership)/ }
    ]
  },
  'b7-controlling-parties': {
    groups: [
      { title: 'Secretary Information', pattern: /^GENSecretary/ },
      { title: 'Fund Manager Details', pattern: /^GEN(UK|Indicative)?.*Fund.*Mng/ },
      { title: 'Investment Adviser Details', pattern: /^GEN(UK|Indicative)?.*Investment.*Adviser/ },
      { title: 'Partnership Structure', pattern: /^GENlimitedpartnership/ }
    ]
  },
  'b5-applicant-details': {
    groups: [
      { title: 'Entity Registration', pattern: /^GEN(UK|Indicative)?.*([Rr]eg|[Cc]ountry[Rr]egistration|[Ff]ormation|[Tt]rading)/ },
      { title: 'Address Information', pattern: /^GEN(UK|Indicative)?.*([Aa]ddress|[Cc]ountry$)/ },
      { title: 'Principal Operations', pattern: /^GEN(UK|Indicative)?.*[Pp]rinc/ },
      { title: 'Business Details', pattern: /^GEN(UK|Indicative)?.*([Bb]usiness|[Oo]perat|[Aa]ctiv)/ }
    ]
  },
  'b6-tax-classification': {
    groups: [
      { title: 'Tax Country & Jurisdiction', pattern: /^GEN.*([Tt]ax[Cc]ountry|[Tt]ax[Cc]omplex)/ },
      { title: 'Tax Identification Numbers', pattern: /^GEN.*([Tt]in|[Gg]iin)/ },
      { title: 'FATCA & CRS Classification', pattern: /^GEN.*(ffi|[Ff]ior|[Ff]atca|[Cc]rs)/ },
      { title: 'Tax Compliance Status', pattern: /^GEN.*([Tt]ax.*[Aa]rrears|[Tt]ax.*[Aa]pplicable)/ }
    ]
  }
}

// Check if section has field grouping configured
function hasFieldGrouping(sectionKey: string): boolean {
  return Boolean(FIELD_GROUPING_CONFIG[sectionKey])
}

// Get field groups for any supported section
function getFieldGroupsForSection(sectionKey: string) {
  const config = FIELD_GROUPING_CONFIG[sectionKey]
  if (!config) {
    return []
  }
  
  const sectionFields = fieldsForAccordion(sectionKey)
  if (sectionFields.length === 0) {
    return []
  }
  
  // Initialize groups
  const groups = config.groups.map(groupConfig => ({
    title: groupConfig.title,
    pattern: groupConfig.pattern,
    fields: []
  }))
  
  // Group fields by patterns
  for (const field of sectionFields) {
    let grouped = false
    for (const group of groups) {
      if (group.pattern.test(field.key)) {
        group.fields.push(field)
        grouped = true
        break
      }
    }
    
    // If field doesn't match any pattern, create "Other" group
    if (!grouped) {
      let otherGroup = groups.find(g => g.title.includes('Other'))
      if (!otherGroup) {
        otherGroup = {
          title: 'Other Fields',
          pattern: /.*/,
          fields: []
        }
        groups.push(otherGroup)
      }
      otherGroup.fields.push(field)
    }
  }
  
  // Sort fields within each group by dependency chains
  for (const group of groups) {
    group.fields = sortFieldsByDependencyChains(group.fields)
  }
  
  // Only return groups that have fields
  return groups.filter(group => group.fields.length > 0)
}

// Sort fields by dependency chains to keep related fields together
function sortFieldsByDependencyChains(fields: any[]): any[] {
  // Build dependency map
  const dependencyMap = new Map<string, string[]>() // child -> [parents]
  const reverseDependencyMap = new Map<string, string[]>() // parent -> [children]
  
  // Analyze visibility rules to build dependency relationships
  for (const field of fields) {
    const fieldKey = field.key
    const dependencies: string[] = []
    
    if (field.visibility && field.visibility.length > 0) {
      for (const rule of field.visibility) {
        for (const condition of (rule.conditions || [])) {
          const parentKey = condition.sourceKey
          if (parentKey && fields.some(f => f.key === parentKey)) {
            dependencies.push(parentKey)
            
            // Add to reverse map
            if (!reverseDependencyMap.has(parentKey)) {
              reverseDependencyMap.set(parentKey, [])
            }
            reverseDependencyMap.get(parentKey)!.push(fieldKey)
          }
        }
      }
    }
    
    if (dependencies.length > 0) {
      dependencyMap.set(fieldKey, dependencies)
    }
  }
  
  // Group fields into dependency chains
  const chains: any[][] = []
  const processed = new Set<string>()
  
  // Find root fields (no dependencies within this group)
  const rootFields = fields.filter(field => 
    !dependencyMap.has(field.key) || 
    dependencyMap.get(field.key)!.every(dep => !fields.some(f => f.key === dep))
  )
  
  // Build chains starting from each root
  for (const rootField of rootFields) {
    if (processed.has(rootField.key)) continue
    
    const chain = buildDependencyChain(rootField, fields, reverseDependencyMap, processed)
    if (chain.length > 0) {
      chains.push(chain)
    }
  }
  
  // Add any remaining unprocessed fields as individual chains
  for (const field of fields) {
    if (!processed.has(field.key)) {
      chains.push([field])
    }
  }
  
  // Sort chains by Paul order of first field in chain, then unconditional first
  chains.sort((chainA, chainB) => {
    const aFirst = chainA[0]
    const bFirst = chainB[0]
    
    // Unconditional chains first
    const aHasVisibility = Boolean(aFirst.visibility && aFirst.visibility.length > 0)
    const bHasVisibility = Boolean(bFirst.visibility && bFirst.visibility.length > 0)
    if (aHasVisibility !== bHasVisibility) {
      return aHasVisibility ? 1 : -1
    }
    
    // Then by Paul order
    const aOrder = aFirst._paul_order || 999
    const bOrder = bFirst._paul_order || 999
    if (aOrder !== bOrder) {
      return aOrder - bOrder
    }
    
    // Finally by field key
    return aFirst.key.localeCompare(bFirst.key)
  })
  
  // Flatten chains back to single array
  return chains.flat()
}

// Recursively build dependency chain from root field
function buildDependencyChain(
  rootField: any, 
  allFields: any[], 
  reverseDependencyMap: Map<string, string[]>, 
  processed: Set<string>
): any[] {
  if (processed.has(rootField.key)) {
    return []
  }
  
  const chain = [rootField]
  processed.add(rootField.key)
  
  // Add children recursively
  const children = reverseDependencyMap.get(rootField.key) || []
  for (const childKey of children) {
    const childField = allFields.find(f => f.key === childKey)
    if (childField && !processed.has(childKey)) {
      const subChain = buildDependencyChain(childField, allFields, reverseDependencyMap, processed)
      chain.push(...subChain)
    }
  }
  
  return chain
}

// Generalized Field Hierarchy CSS Classes
function getFieldHierarchyClass(field: any) {
  const key = field.key
  
  // Child fields (names, domicile, location, address, etc.)
  if (key.includes('Name') || key.includes('Dom') || key.includes('Location') || 
      key.includes('address') || key.includes('Address') || key.includes('Country')) {
    return 'field-level-1'
  }
  
  // Grandchild fields (Delaware questions, specific details)
  if (key.includes('USA') || key.includes('Delaware') || 
      key.includes('different') || key.includes('Detail')) {
    return 'field-level-2'
  }
  
  // Parent fields (default)
  return 'field-level-0'
}

// Visibility evaluation
function evaluateVisibility(field: any): boolean {
  if (!field.visibility || field.visibility.length === 0) return true
  
  for (const rule of field.visibility) {
    const conditions = rule.conditions || []
    const allMatch = rule.allConditionsMustMatch !== false // default true
    
    if (allMatch) {
      // All conditions must match (AND)
      const allPass = conditions.every((cond: any) => {
        const sourceValue = formData[cond.sourceKey]
        const targetValue = cond.value
        const sv = typeof sourceValue === 'string' ? sourceValue.toLowerCase() : sourceValue
        const tv = typeof targetValue === 'string' ? targetValue.toLowerCase() : targetValue
        if (cond.operator === 'eq' || cond.operator === '==') {
          return sv == tv
        } else if (cond.operator === 'neq' || cond.operator === '!=') {
          return sv != tv
        }
        return true
      })
      if (allPass) return true
    } else {
      // Any condition can match (OR)
      const anyPass = conditions.some((cond: any) => {
        const sourceValue = formData[cond.sourceKey]
        const targetValue = cond.value
        const sv = typeof sourceValue === 'string' ? sourceValue.toLowerCase() : sourceValue
        const tv = typeof targetValue === 'string' ? targetValue.toLowerCase() : targetValue
        if (cond.operator === 'eq' || cond.operator === '==') {
          return sv == tv
        } else if (cond.operator === 'neq' || cond.operator === '!=') {
          return sv != tv
        }
        return false
      })
      if (anyPass) return true
    }
  }
  
  return false
}

const visibleFields = computed(() => displayFields.value.filter(field => evaluateVisibility(field)))

function groupSection(g: any): string {
  const firstChild = (g.children || []).map((k: string) => fieldMap.value[k]).find(Boolean)
  return firstChild?._section || 'General'
}
function groupsForSection(section: string) {
  return (groups.value || [])
    .filter((g: any) => groupSection(g) === section)
    // If complex parent field exists, respect its visibility
    .filter((g: any) => {
      const parent = fieldMap.value[g.key]
      return !parent || parent.type !== 'complex' || evaluateVisibility(parent)
    })
    .filter((g: any) => groupChildFields(g).length > 0)
}
function groupsForAccordion(accordionKey: string) {
  return (groups.value || [])
    .filter((g: any) => {
      const sectionSlug = slugify(groupSection(g))
      return sectionSlug === accordionKey || accordionKeyForField(fieldMap.value[g.key]) === accordionKey
    })
    .filter((g: any) => {
      const parent = fieldMap.value[g.key]
      return !parent || parent.type !== 'complex' || evaluateVisibility(parent)
    })
    .filter((g: any) => groupChildFields(g).length > 0)
}

function copyOriginal(field: any) {
  return {
    label: field.original?.label ?? field.label ?? null,
    help: field.original?.help ?? field.help ?? field.description ?? null
  }
}

function copyFuture(field: any): { label: string | null; help: string | null; source: string | null; rationale: string | null } | null {
  const future = field?.future
  if (!future) return null
  const label = (future.proposedLabel || '').trim()
  const help = (future.proposedHelp || '').trim()
  return {
    label: label ? label : null,
    help: help ? help : null,
    source: future.changeSource ?? null,
    rationale: future.rationale ?? null
  }
}

function displayLabel(field: any) {
  return copyFuture(field)?.label || field.label
}

function displayHelp(field: any) {
  const future = copyFuture(field)?.help
  if (future) return future
  return field.help || field.description || null
}

function optionChanges(field: any) {
  const options = field.options || []
  return options
    .map((opt: any) => {
      const original = typeof opt.value === 'string' ? opt.value : null
      const updated = opt.label
      if (!original || !updated || original === updated) return null
      return { original, updated }
    })
    .filter(Boolean)
}

function hasCopyChange(field: any): boolean {
  return Boolean(field?.future)
}
function groupChildFields(g: any) {
  return (g.children || [])
    .map((k: string) => fieldMap.value[k])
    .filter((f: any) => !!f && !f.internal && !f.internal_only)
}
function evaluateVisibilityForModel(field: any, model: Record<string, any>) {
  if (!field.visibility || field.visibility.length === 0) return true
  for (const rule of field.visibility) {
    const conditions = rule.conditions || []
    const allMatch = rule.allConditionsMustMatch !== false
    const test = (cond: any) => {
      const sourceValue = (cond.sourceKey in model) ? model[cond.sourceKey] : formData[cond.sourceKey]
      const targetValue = cond.value
      const sv = typeof sourceValue === 'string' ? sourceValue.toLowerCase() : sourceValue
      const tv = typeof targetValue === 'string' ? targetValue.toLowerCase() : targetValue
      if (cond.operator === 'eq' || cond.operator === '==') return sv == tv
      if (cond.operator === 'neq' || cond.operator === '!=') return sv != tv
      return true
    }
    if (allMatch) { if (!conditions.every(test)) return false } else { if (!conditions.some(test)) return false }
  }
  return true
}

// Build a per-condition explanation for a field (optionally within a row model)
function conditionsForField(field: any, model?: Record<string, any>) {
  const out: Array<{ sourceKey: string; operator: string; value: any; current: any; pass: boolean }> = []
  if (!field.visibility || field.visibility.length === 0) return out
  const get = (key: string) => (model && (key in model)) ? model[key] : formData[key]
  for (const rule of field.visibility) {
    for (const cond of (rule.conditions || [])) {
      const svRaw = get(cond.sourceKey)
      const tvRaw = cond.value
      const sv = typeof svRaw === 'string' ? svRaw.toLowerCase() : svRaw
      const tv = typeof tvRaw === 'string' ? tvRaw.toLowerCase() : tvRaw
      let pass = true
      if (cond.operator === 'eq' || cond.operator === '==') pass = sv == tv
      else if (cond.operator === 'neq' || cond.operator === '!=') pass = sv != tv
      out.push({ sourceKey: cond.sourceKey, operator: cond.operator, value: cond.value, current: svRaw ?? '(unset)', pass })
    }
  }
  return out
}

// Sections (order of first appearance); used as dividers only
const sections = computed(() => {
  const sectionSet = new Set<string>()
  const sectionOrder: string[] = []
  for (const field of visibleFields.value) {
    const section = field._section || 'General'
    if (!sectionSet.has(section)) {
      sectionSet.add(section)
      sectionOrder.push(section)
    }
  }
  return sectionOrder.length > 0 ? sectionOrder : ['General']
})

function fieldsBySection(section: string) {
  return visibleFields.value.filter((field: any) => (field._section || 'General') === section)
}

// Validation
function validateAll(): boolean {
  // Clear all errors
  for (const key of Object.keys(errors)) delete errors[key]
  let isValid = true
  for (const field of visibleFields.value) {
    if (field.validation?.required && !formData[field.key]) {
      errors[field.key] = `${displayLabel(field)} is required`
      isValid = false
    }
    
    // Add more validation rules as needed
    if (field.type === 'integer' && formData[field.key]) {
      const value = Number(formData[field.key])
      if (isNaN(value) || !Number.isInteger(value)) {
        errors[field.key] = `${displayLabel(field)} must be a whole number`
        isValid = false
      }
    }
    
    if (field.type === 'decimal' && formData[field.key]) {
      const value = Number(formData[field.key])
      if (isNaN(value)) {
        errors[field.key] = `${displayLabel(field)} must be a number`
        isValid = false
      }
    }
  }
  return isValid
}

function submitForm() {
  if (validateAll()) {
    // For now, just show success
    alert('Form submitted successfully!')
    console.log('Form data:', formData)
  } else {
    const errorEl = document.querySelector('.error-summary')
    if (errorEl) {
      errorEl.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }
}
</script>

<style scoped>
.preview-container {
  min-height: 100vh;
  background: #f8f9fa;
}

.preview-header {
  background: white;
  border-bottom: 1px solid #e1e4e8;
  padding: 24px 0;
  margin-bottom: 32px;
}

.preview-header-content {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 24px;
}

.back-link {
  display: inline-block;
  margin-bottom: 12px;
  color: #0969da;
  text-decoration: none;
  font-size: 14px;
}

.back-link:hover {
  text-decoration: underline;
}

h1 {
  margin: 0 0 8px;
  font-size: 32px;
  font-weight: 600;
  color: #0d1117;
}

.journey-meta {
  margin: 0;
  color: #57606a;
  font-size: 14px;
}

.error-message {
  max-width: 800px;
  margin: 32px auto;
  padding: 24px;
  background: #ffebe9;
  border: 1px solid #ff8182;
  border-radius: 6px;
}

.error-message strong {
  color: #cf222e;
}

.preview-content {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 24px 48px;
}

.step-nav {
  display: flex;
  gap: 24px;
  margin-bottom: 32px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  overflow-x: auto;
}

.step-button {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #57606a;
  white-space: nowrap;
  transition: all 0.2s;
}

.step-button:hover {
  color: #0d1117;
}

.step-button--active {
  color: #0969da;
  font-weight: 600;
}

.step-button--completed {
  color: #1a7f37;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #f0f3f6;
  font-weight: 600;
  font-size: 12px;
}

.step-button--active .step-number {
  background: #0969da;
  color: white;
}

.step-button--completed .step-number {
  background: #1a7f37;
  color: white;
}

.form-container {
  background: white;
  border-radius: 8px;
  padding: 32px;
}

.accordion-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 8px 0 24px;
}

.accordion-empty {
  padding: 16px 18px;
  border: 1px dashed #cbd5e1;
  border-radius: 8px;
  background: #f8fafc;
  color: #475569;
}

.accordion-empty__title {
  margin: 0 0 6px;
  font-size: 14px;
  font-weight: 600;
}

.accordion-empty__hint {
  margin: 0;
  font-size: 13px;
  color: #64748b;
}


.tools {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #57606a;
}

.debug-explain {
  margin: 6px 0 16px 0;
  padding: 8px 10px;
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: 6px;
}
.debug-explain .debug-title { font-weight: 600; font-size: 12px; margin-bottom: 6px; }
.debug-explain .muted { color: #6b7280; font-size: 12px; }
.debug-explain .pass { color: #16a34a; margin-right: 6px; }
.debug-explain .fail { color: #dc2626; margin-right: 6px; }
.debug-copy { margin-bottom: 10px; }
.debug-row { margin: 0 0 4px; font-size: 13px; line-height: 1.4; }
.debug-label { font-weight: 600; }
.debug-meta { margin: 4px 0 0; font-size: 12px; color: #475569; }
.debug-explain ul { margin: 0; padding-left: 16px; font-size: 12px; color: #475569; }
.debug-explain li { margin-bottom: 4px; }

/* Field Key Display Styling */
.debug-field-info {
  margin-bottom: 8px;
  padding-bottom: 6px;
  border-bottom: 1px solid #e2e8f0;
}

.debug-field-key {
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  background: var(--kycp-gray-100, #f3f4f6);
  color: var(--kycp-gray-800, #1f2937);
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.02em;
}

.error-summary {
  margin-bottom: 24px;
  padding: 16px;
  background: #ffebe9;
  border: 1px solid #ff8182;
  border-radius: 6px;
}

.error-summary h3 {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 600;
  color: #cf222e;
}

.error-summary ul {
  margin: 0;
  padding-left: 20px;
}

.error-summary li {
  margin: 4px 0;
  color: #cf222e;
  font-size: 14px;
}

.form-section {
  margin-bottom: 32px;
}

.field-container {
}

.form-actions {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding-top: 24px;
  border-top: 1px solid #e1e4e8;
}

/* Floating tools */
.floating-tools {
  position: fixed;
  right: 24px;
  bottom: 24px;
  background: white;
  border: 1px solid #e1e4e8;
  border-radius: 999px;
  padding: 8px 12px;
  box-shadow: 0 8px 24px rgba(140,149,159,0.2);
  font-size: 13px;
  color: #57606a;
  z-index: 1000;
}

@media (max-width: 640px) {
  .floating-tools {
    right: 12px;
    bottom: 12px;
    padding: 8px 10px;
    font-size: 12px;
  }
}

/* Generalized Field Grouping Styles */
.field-group {
  margin-bottom: 32px;
}

.field-group-header {
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--kycp-primary-100, #e3f2fd);
}

.field-group-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--kycp-primary-700, #1976d2);
  display: flex;
  align-items: center;
  gap: 8px;
}

.field-group-content {
  padding-left: 8px;
}

/* Generalized Field Hierarchy Classes */
.field-level-0 {
  /* Parent fields - no extra indentation */
}

.field-level-1 {
  /* Child fields - indented */
  margin-left: 24px;
  position: relative;
}

.field-level-1::before {
  /* Visual connector line for child fields */
  content: '';
  position: absolute;
  left: -16px;
  top: 8px;
  width: 12px;
  height: 1px;
  background: var(--kycp-gray-300, #d1d5db);
}

.field-level-2 {
  /* Grandchild fields - double indented */
  margin-left: 48px;
  position: relative;
}

.field-level-2::before {
  /* Visual connector line for grandchild fields */
  content: '';
  position: absolute;
  left: -16px;
  top: 8px;
  width: 12px;
  height: 1px;
  background: var(--kycp-gray-300, #d1d5db);
}

/* Additional spacing between field groups */
.field-group:not(:last-child) {
  border-bottom: 1px solid var(--kycp-gray-100, #f3f4f6);
  padding-bottom: 24px;
}

/* Improve readability of nested fields */
.field-level-1 .kycp-field-wrapper__label,
.field-level-2 .kycp-field-wrapper__label {
  font-size: 14px;
  color: var(--kycp-gray-700, #374151);
}

.field-level-0 .kycp-field-wrapper__label {
  font-size: 15px;
  font-weight: 500;
  color: var(--kycp-gray-900, #111827);
}
</style>
