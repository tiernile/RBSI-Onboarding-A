<template>
  <div class="component-library">
    <header class="library-header">
      <NuxtLink to="/" class="back-link">← Mission Control</NuxtLink>
      <h1>Component Library</h1>
      <p class="subtitle">Pure UI components for form building</p>
    </header>

    <nav class="library-nav">
      <a href="#field-components" class="nav-link">Field Components</a>
      <a href="#non-input" class="nav-link">Non-Input Components</a>
      <a href="#complex" class="nav-link">Complex Groups</a>
      <a href="#limits" class="nav-link">Platform Limits</a>
      <a href="#visibility" class="nav-link">Visibility & Rights</a>
      <a href="#modal" class="nav-link">Modal (Prototype Only)</a>
    </nav>

    <main class="library-content">
      <!-- Text Input -->
      <section id="text-input" class="component-section">
        <h2>Text Input</h2>
        <p class="section-description">Basic text input field for single-line text entry.</p>
        
        <div class="example-grid">
          <div class="example">
            <h3>Default</h3>
            <KycpInput 
              v-model="examples.text.default" 
              placeholder="Enter text..."
            />
            <code>{{ examples.text.default || '(empty)' }}</code>
          </div>

          <div class="example">
            <h3>With Label</h3>
            <KycpFieldWrapper label="Full Name" :required="true">
              <KycpInput 
                v-model="examples.text.labeled" 
                placeholder="John Smith"
              />
            </KycpFieldWrapper>
          </div>

          <div class="example">
            <h3>With Help Text</h3>
            <KycpFieldWrapper 
              label="Email Address" 
              help="We'll never share your email"
            >
              <KycpInput 
                v-model="examples.text.help" 
                type="email"
                placeholder="john@example.com"
              />
            </KycpFieldWrapper>
          </div>

          <div class="example">
            <h3>With Error</h3>
            <KycpFieldWrapper 
              label="Username" 
              error="Username is already taken"
              :required="true"
            >
              <KycpInput 
                v-model="examples.text.error" 
                :error="true"
              />
            </KycpFieldWrapper>
          </div>
        </div>
      </section>

      <!-- Textarea -->
      <section id="textarea" class="component-section">
        <h2>Textarea</h2>
        <p class="section-description">Multi-line text input for longer content.</p>
        
        <div class="example-grid">
          <div class="example">
            <h3>Default</h3>
            <KycpTextarea 
              v-model="examples.textarea.default" 
              placeholder="Enter description..."
              :rows="4"
            />
          </div>

          <div class="example">
            <h3>With Character Count</h3>
            <KycpFieldWrapper 
              label="Description" 
              help="Maximum 500 characters"
            >
              <KycpTextarea 
                v-model="examples.textarea.counted" 
                :maxlength="500"
                :rows="4"
              />
            </KycpFieldWrapper>
            <small>{{ examples.textarea.counted?.length || 0 }}/500</small>
          </div>
        </div>
      </section>

      <!-- Select -->
      <section id="select" class="component-section">
        <h2>Select Dropdown</h2>
        <p class="section-description">Dropdown selection from predefined options.</p>
        
        <div class="example-grid">
          <div class="example">
            <h3>Default</h3>
            <KycpSelect 
              v-model="examples.select.default"
              :options="countryOptions"
              placeholder="Select country..."
            />
            <code>Selected: {{ examples.select.default || 'none' }}</code>
          </div>

          <div class="example">
            <h3>With Label</h3>
            <KycpFieldWrapper label="Country" :required="true">
              <KycpSelect 
                v-model="examples.select.labeled"
                :options="countryOptions"
                placeholder="Choose a country"
              />
            </KycpFieldWrapper>
          </div>

          <div class="example">
            <h3>Disabled Options</h3>
            <KycpFieldWrapper label="Tier">
              <KycpSelect 
                v-model="examples.select.disabled"
                :options="tierOptions"
              />
            </KycpFieldWrapper>
          </div>
        </div>
      </section>

      <!-- Number Inputs -->
      <section id="number" class="component-section">
        <h2>Number Inputs</h2>
        <p class="section-description">Integer and decimal inputs with validation.</p>
        
        <div class="example-grid">
          <div class="example">
            <h3>Integer</h3>
            <KycpFieldWrapper label="Employee Count" help="Whole numbers only">
              <KycpInput 
                v-model="examples.number.integer" 
                type="number"
                placeholder="0"
              />
            </KycpFieldWrapper>
            <code>Value: {{ examples.number.integer || 0 }}</code>
          </div>

          <div class="example">
            <h3>Decimal (2 places)</h3>
            <KycpFieldWrapper label="Annual Turnover" help="Maximum 2 decimal places">
              <KycpInput 
                v-model="examples.number.decimal" 
                type="number"
                step="0.01"
                placeholder="0.00"
              />
            </KycpFieldWrapper>
            <code>Value: {{ examples.number.decimal || 0 }}</code>
          </div>
        </div>
      </section>

      <!-- Date Input -->
      <section id="date" class="component-section">
        <h2>Date Input</h2>
        <p class="section-description">Date picker with DD/MM/YYYY format.</p>
        
        <div class="example-grid">
          <div class="example">
            <h3>Basic Date</h3>
            <KycpFieldWrapper label="Date of Birth" :required="true">
              <KycpInput 
                v-model="examples.date.basic" 
                type="date"
                placeholder="DD/MM/YYYY"
              />
            </KycpFieldWrapper>
            <code>Value: {{ examples.date.basic || 'not set' }}</code>
          </div>

          <div class="example">
            <h3>Expiry Date</h3>
            <KycpFieldWrapper label="Document Expiry" help="Must be in the future">
              <KycpInput 
                v-model="examples.date.expiry" 
                type="date"
                placeholder="DD/MM/YYYY"
              />
            </KycpFieldWrapper>
          </div>
        </div>
      </section>

      <!-- Note: Radio components removed - KYCP uses dropdowns only -->

      <!-- Field Wrapper -->
      <section id="field-wrapper" class="component-section">
        <h2>Field Wrapper</h2>
        <p class="section-description">Container that adds label, help text, and error messages to any input.</p>
        
        <div class="example-grid">
          <div class="example">
            <h3>All Features</h3>
            <KycpFieldWrapper 
              label="Account Number"
              help="Enter your 8-digit account number"
              error="Invalid account number format"
              :required="true"
            >
              <KycpInput 
                v-model="examples.wrapper.full"
                :error="true"
                placeholder="12345678"
              />
            </KycpFieldWrapper>
          </div>

          <div class="example">
            <h3>Optional Field</h3>
            <KycpFieldWrapper 
              label="Middle Name"
              help="Optional"
            >
              <KycpInput 
                v-model="examples.wrapper.optional"
              />
            </KycpFieldWrapper>
          </div>

          <div class="example">
            <h3>Grouped Fields</h3>
            <KycpFieldGroup title="Personal Information" subtitle="Please provide your details">
              <KycpFieldWrapper label="First Name" :required="true">
                <KycpInput v-model="examples.wrapper.grouped1" />
              </KycpFieldWrapper>
              <KycpFieldWrapper label="Last Name" :required="true">
                <KycpInput v-model="examples.wrapper.grouped2" />
              </KycpFieldWrapper>
            </KycpFieldGroup>
          </div>
        </div>
      </section>

      <!-- Buttons -->
      <section id="buttons" class="component-section">
        <h2>Buttons</h2>
        <p class="section-description">Action buttons in various styles and states.</p>
        
        <div class="example-grid">
          <div class="example">
            <h3>Primary</h3>
            <div style="display: flex; gap: 12px;">
              <KycpButton variant="primary">Upload</KycpButton>
              <KycpButton variant="primary" :disabled="true">Disabled</KycpButton>
              <KycpButton variant="primary" :loading="true">Loading</KycpButton>
            </div>
          </div>

          <div class="example">
            <h3>Secondary</h3>
            <div style="display: flex; gap: 12px;">
              <KycpButton variant="secondary">Cancel</KycpButton>
              <KycpButton variant="secondary" :disabled="true">Disabled</KycpButton>
            </div>
          </div>

          <div class="example">
            <h3>Text Button</h3>
            <div style="display: flex; gap: 12px;">
              <KycpButton variant="text">ADD NEW...</KycpButton>
              <KycpButton variant="text">View Details</KycpButton>
            </div>
          </div>
        </div>
      </section>

      <!-- Section -->
      <section id="section" class="component-section">
        <h2>Section Component</h2>
        <p class="section-description">Form sections with headers and descriptions.</p>
        
        <div class="example">
          <KycpSection 
            title="Business Activity"
            description="Please complete the following questions as accurately as possible and provide full answers where possible. The quality of the information you provide in this application will directly impact the time that it takes for your account to be opened."
            instructions="Please provide full answers to each of the questions below. If full answers are not provided your application may be delayed."
          >
            <KycpFieldWrapper label="Business activity" :required="true">
              <KycpSelect 
                v-model="examples.section.activity"
                :options="businessOptions"
                placeholder="Select activity..."
              />
            </KycpFieldWrapper>
          </KycpSection>
        </div>
      </section>

      <!-- Repeater -->
      <section id="repeater" class="component-section">
        <h2>Repeater Component</h2>
        <p class="section-description">Complex groups with ADD NEW... pattern for repeating data.</p>
        
        <div class="example">
          <h3>ID Documents Example</h3>
          <KycpRepeater
            v-model="examples.repeater.documents"
            item-label="Document"
            add-label="Document Details"
            title-field="type"
          >
            <template #item="{ item }">
              <div style="display: grid; gap: 16px;">
                <KycpFieldWrapper label="Document Type">
                  <KycpInput v-model="item.type" readonly />
                </KycpFieldWrapper>
                <KycpFieldWrapper label="Document Number">
                  <KycpInput v-model="item.number" readonly />
                </KycpFieldWrapper>
              </div>
            </template>
            
            <template #form="{ item, save, cancel }">
              <div style="display: grid; gap: 16px;">
                <KycpFieldWrapper label="Document Type" :required="true">
                  <KycpSelect 
                    v-model="item.type"
                    :options="['Passport', 'Driver License', 'ID Card']"
                    placeholder="Select type..."
                  />
                </KycpFieldWrapper>
                <KycpFieldWrapper label="Document Number" :required="true">
                  <KycpInput 
                    v-model="item.number"
                    placeholder="Enter document number"
                  />
                </KycpFieldWrapper>
                <KycpFieldWrapper label="Expiry Date">
                  <KycpInput 
                    v-model="item.expiry"
                    type="date"
                    placeholder="DD/MM/YYYY"
                  />
                </KycpFieldWrapper>
                <div style="display: flex; gap: 12px; justify-content: flex-end;">
                  <KycpButton variant="secondary" @click="cancel">Cancel</KycpButton>
                  <KycpButton variant="primary" @click="save">Save</KycpButton>
                </div>
              </div>
            </template>
          </KycpRepeater>
        </div>
      </section>

      <!-- Modal -->
      <section id="modal" class="component-section">
        <h2>Modal Component</h2>
        <p class="section-description">Overlay dialogs for uploads and confirmations.</p>
        
        <div class="example">
          <KycpButton variant="primary" @click="showModal = true">Open Upload Modal</KycpButton>
          
          <KycpModal 
            v-model="showModal" 
            title="UPLOAD DOCUMENT"
            icon="↑"
          >
            <div style="display: grid; gap: 20px;">
              <h3 style="margin: 0; font-size: 16px; color: var(--kycp-gray-700);">Document Details:</h3>
              
              <KycpFieldWrapper label="Description" :required="true">
                <KycpInput placeholder="Enter description" />
              </KycpFieldWrapper>
              
              <KycpFieldWrapper label="Doc Type">
                <KycpSelect 
                  :options="['Passport', 'Proof of Address', 'Bank Statement']"
                  placeholder="Select..."
                />
              </KycpFieldWrapper>
              
              <KycpFieldWrapper label="Expiry Date">
                <KycpInput type="date" placeholder="DD/MM/YYYY" />
              </KycpFieldWrapper>
              
              <KycpFieldWrapper label="File Upload">
                <div style="display: flex; gap: 12px; align-items: center;">
                  <input type="file" style="flex: 1;" />
                  <KycpButton variant="primary">BROWSE</KycpButton>
                </div>
              </KycpFieldWrapper>
            </div>
            
            <template #footer>
              <KycpButton variant="secondary" @click="showModal = false">CANCEL</KycpButton>
              <KycpButton variant="primary" @click="showModal = false">UPLOAD</KycpButton>
            </template>
          </KycpModal>
        </div>
      </section>

      <!-- KYCP Patterns -->
      <section id="patterns" class="component-section">
        <h2>KYCP Patterns</h2>
        <p class="section-description">Common patterns from the KYCP platform.</p>
        
        <div class="example">
          <h3>PEP Follow-up Pattern</h3>
          <p style="margin-bottom: 20px; color: var(--kycp-gray-600); font-size: 14px;">
            Yes/No lookup followed by conditional text explanation
          </p>
          <KycpFieldWrapper label="Are you a Politically Exposed Person (PEP)?" :required="true">
            <KycpSelect 
              v-model="examples.patterns.pep"
              :options="yesNoOptions"
              placeholder="Select..."
            />
          </KycpFieldWrapper>
          
          <div v-if="examples.patterns.pep === 'yes'" style="margin-top: 16px;">
            <KycpFieldWrapper 
              label="Please provide details" 
              :required="true"
              help="Explain your PEP status and any relevant positions"
            >
              <KycpTextarea 
                v-model="examples.patterns.pepDetails"
                :rows="4"
                placeholder="Provide details..."
              />
            </KycpFieldWrapper>
          </div>
        </div>
      </section>

      <!-- States -->
      <section id="states" class="component-section">
        <h2>Component States</h2>
        <p class="section-description">Visual states for all components.</p>
        
        <div class="states-grid">
          <div class="state-example">
            <h3>Default</h3>
            <KycpInput placeholder="Default state" />
          </div>

          <div class="state-example">
            <h3>Hover</h3>
            <KycpInput placeholder="Hover over me" />
          </div>

          <div class="state-example">
            <h3>Focus</h3>
            <KycpInput placeholder="Click to focus" />
          </div>

          <div class="state-example">
            <h3>Filled</h3>
            <KycpInput v-model="filledValue" />
          </div>

          <div class="state-example">
            <h3>Disabled</h3>
            <KycpInput placeholder="Disabled" :disabled="true" />
          </div>

          <div class="state-example">
            <h3>Read Only</h3>
            <KycpInput value="Read only value" :readonly="true" />
          </div>

          <div class="state-example">
            <h3>Error</h3>
            <KycpInput placeholder="Error state" :error="true" />
          </div>

          <div class="state-example">
            <h3>Required</h3>
            <KycpFieldWrapper label="Required Field" :required="true">
              <KycpInput placeholder="This field is required" />
            </KycpFieldWrapper>
          </div>
        </div>
      </section>

      <!-- Props Documentation -->
      <section class="component-section">
        <h2>Component Props</h2>
        
        <div class="props-table">
          <h3>KycpInput</h3>
          <table>
            <thead>
              <tr>
                <th>Prop</th>
                <th>Type</th>
                <th>Default</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>modelValue</td>
                <td>string | number</td>
                <td>-</td>
                <td>Input value (v-model)</td>
              </tr>
              <tr>
                <td>type</td>
                <td>text | email | tel | number | password | url</td>
                <td>text</td>
                <td>Input type</td>
              </tr>
              <tr>
                <td>placeholder</td>
                <td>string</td>
                <td>-</td>
                <td>Placeholder text</td>
              </tr>
              <tr>
                <td>disabled</td>
                <td>boolean</td>
                <td>false</td>
                <td>Disable input</td>
              </tr>
              <tr>
                <td>readonly</td>
                <td>boolean</td>
                <td>false</td>
                <td>Make input read-only</td>
              </tr>
              <tr>
                <td>error</td>
                <td>boolean</td>
                <td>false</td>
                <td>Show error state</td>
              </tr>
              <tr>
                <td>maxlength</td>
                <td>number</td>
                <td>-</td>
                <td>Maximum character length</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="props-table">
          <h3>KycpFieldWrapper</h3>
          <table>
            <thead>
              <tr>
                <th>Prop</th>
                <th>Type</th>
                <th>Default</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>label</td>
                <td>string</td>
                <td>-</td>
                <td>Field label</td>
              </tr>
              <tr>
                <td>help</td>
                <td>string</td>
                <td>-</td>
                <td>Help text below input</td>
              </tr>
              <tr>
                <td>error</td>
                <td>string</td>
                <td>-</td>
                <td>Error message</td>
              </tr>
              <tr>
                <td>required</td>
                <td>boolean</td>
                <td>false</td>
                <td>Show required indicator</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import KycpInput from '~/components/kycp/base/KycpInput.vue'
import KycpTextarea from '~/components/kycp/base/KycpTextarea.vue'
import KycpSelect from '~/components/kycp/base/KycpSelect.vue'
import KycpFieldWrapper from '~/components/kycp/base/KycpFieldWrapper.vue'
import KycpFieldGroup from '~/components/kycp/base/KycpFieldGroup.vue'
import KycpStatement from '~/components/kycp/base/KycpStatement.vue'
import KycpDivider from '~/components/kycp/base/KycpDivider.vue'
import KycpRepeater from '~/components/kycp/base/KycpRepeater.vue'
import KycpModal from '~/components/kycp/base/KycpModal.vue'
import KycpButton from '~/components/kycp/base/KycpButton.vue'

// Example data
const filledValue = ref('Example text')
const showModal = ref(false)

const examples = ref({
  text: {
    default: '',
    labeled: '',
    help: '',
    error: 'admin'
  },
  textarea: {
    default: '',
    counted: ''
  },
  number: {
    integer: null,
    decimal: null
  },
  date: {
    basic: '',
    expiry: ''
  },
  select: {
    default: '',
    labeled: '',
    disabled: ''
  },
  radio: {
    default: '',
    horizontal: '',
    multiple: ''
  },
  wrapper: {
    full: '1234',
    optional: '',
    grouped1: '',
    grouped2: ''
  },
  section: {
    activity: ''
  },
  repeater: {
    documents: []
  },
  patterns: {
    pep: '',
    pepDetails: ''
  }
})

// Options for dropdowns
const countryOptions = [
  { value: 'uk', label: 'United Kingdom' },
  { value: 'us', label: 'United States' },
  { value: 'de', label: 'Germany' },
  { value: 'fr', label: 'France' },
  { value: 'jp', label: 'Japan' }
]

const tierOptions = [
  { value: 'basic', label: 'Basic' },
  { value: 'standard', label: 'Standard' },
  { value: 'premium', label: 'Premium', disabled: true },
  { value: 'enterprise', label: 'Enterprise', disabled: true }
]

const yesNoOptions = [
  { value: 'yes', label: 'Yes' },
  { value: 'no', label: 'No' }
]

const riskOptions = [
  { value: 'low', label: 'Low Risk' },
  { value: 'medium', label: 'Medium Risk' },
  { value: 'high', label: 'High Risk' },
  { value: 'critical', label: 'Critical Risk' }
]

const businessOptions = [
  { value: 'holding', label: 'Company holding' },
  { value: 'investment', label: 'Investment management' },
  { value: 'real-estate', label: 'Real estate' },
  { value: 'trading', label: 'Trading' },
  { value: 'other', label: 'Other' }
]
</script>

<style scoped>
.component-library {
  min-height: 100vh;
  background: var(--color-bg);
}

.library-header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: 32px;
}

.back-link {
  display: inline-block;
  margin-bottom: 16px;
  color: var(--color-link);
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}

h1 {
  margin: 0 0 8px;
  font-size: 32px;
  color: var(--color-text-primary);
}

.subtitle {
  margin: 0;
  color: var(--color-text-secondary);
}

.library-nav {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: 0 32px;
  display: flex;
  gap: 32px;
  overflow-x: auto;
}

.nav-link {
  display: block;
  padding: 16px 0;
  color: var(--color-text-secondary);
  text-decoration: none;
  border-bottom: 2px solid transparent;
  white-space: nowrap;
}

.nav-link:hover {
  color: var(--color-text-primary);
  border-bottom-color: var(--color-border);
}

.library-content {
  padding: 48px 32px;
  max-width: 1400px;
  margin: 0 auto;
}

.component-section {
  margin-bottom: 80px;
}

.component-section h2 {
  margin: 0 0 8px;
  font-size: 28px;
  color: var(--color-text-primary);
}

.section-description {
  margin: 0 0 32px;
  color: var(--color-text-secondary);
  font-size: 16px;
}

.example-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
}

.example {
  background: var(--color-surface);
  padding: 24px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
}

.example h3 {
  margin: 0 0 16px;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.example code {
  display: block;
  margin-top: 12px;
  padding: 8px;
  background: var(--color-bg);
  border-radius: 4px;
  font-size: 12px;
  color: var(--color-text-secondary);
}

.example small {
  display: block;
  margin-top: 8px;
  color: var(--color-text-secondary);
  text-align: right;
}

.states-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 24px;
}

.state-example {
  background: var(--color-surface);
  padding: 20px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
}

.state-example h3 {
  margin: 0 0 12px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.props-table {
  margin-bottom: 48px;
}

.props-table h3 {
  margin: 0 0 16px;
  font-size: 20px;
  color: var(--color-text-primary);
}

.props-table table {
  width: 100%;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
}

.props-table th {
  background: var(--color-bg);
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: var(--color-text-primary);
  border-bottom: 1px solid var(--color-border);
}

.props-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-secondary);
}

.props-table tr:last-child td {
  border-bottom: none;
}

.props-table td:first-child {
  font-family: monospace;
  color: var(--color-text-primary);
  font-weight: 500;
}
</style>