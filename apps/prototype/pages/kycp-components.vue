<template>
  <div class="component-library">
    <header class="library-header">
      <NuxtLink to="/" class="back-link">← Mission Control</NuxtLink>
      <h1>KYCP Component Library</h1>
      <p class="subtitle">Component styles and data types matching KYCP platform</p>
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
      <!-- Field Components -->
      <section id="field-components" class="component-section">
        <h2>Field Components (Data Capture)</h2>
        <p class="section-description">
          KYCP supports exactly 6 data types for field components: 
          <strong>string</strong>, <strong>integer</strong>, <strong>decimal</strong>, 
          <strong>date</strong>, <strong>lookup</strong>, and <strong>freeText</strong>.
        </p>
        
        <!-- Example matching screenshot -->
        <div class="example">
          <h3>KYCP Form Example (Matching Platform)</h3>
          
          <!-- Section Divider -->
          <KycpDivider title="Details of new customer account ('the entity')" />
          
          <!-- Statement -->
          <KycpStatement 
            text="Please complete the following questions as accurately as possible and provide full answers where possible. The quality of the information you provide in this application will directly impact the time that it takes for your account to be opened."
          />
          
          <!-- Another Section -->
          <KycpDivider title="Fund Details (CIS)" />
          
          <!-- Name field -->
          <KycpFieldWrapper label="Name of fund (CIS) entity (in full)" :required="true">
            <KycpInput 
              v-model="examples.fundName" 
              placeholder=""
            />
          </KycpFieldWrapper>
          
          <!-- Type field with description -->
          <KycpFieldWrapper 
            label="Type of Fund" 
            :required="true"
            :description="fundTypeDescription"
          >
            <KycpSelect 
              v-model="examples.fundType"
              :options="fundTypeOptions"
              placeholder="None Selected"
            />
          </KycpFieldWrapper>
        </div>

        <!-- String -->
        <div class="example">
          <h3>String (max 1,024 chars)</h3>
          <KycpFieldWrapper label="Company Name" :required="true">
            <KycpInput 
              v-model="examples.string" 
              :maxlength="1024"
              placeholder="Enter company name"
            />
          </KycpFieldWrapper>
          <code>Value: {{ examples.string || '(empty)' }} | Length: {{ examples.string?.length || 0 }}/1024</code>
        </div>

        <!-- FreeText -->
        <div class="example">
          <h3>FreeText (max 8,192 chars)</h3>
          <KycpFieldWrapper 
            label="Business Description" 
            help="Provide detailed description of business activities"
          >
            <KycpTextarea 
              v-model="examples.freeText" 
              :maxlength="8192"
              :rows="4"
              placeholder="Enter description..."
            />
          </KycpFieldWrapper>
          <code>Length: {{ examples.freeText?.length || 0 }}/8192</code>
        </div>

        <!-- Integer -->
        <div class="example">
          <h3>Integer (0 to 2,147,483,647)</h3>
          <KycpFieldWrapper label="Number of Employees">
            <KycpInput 
              v-model="examples.integer" 
              type="number"
              :min="0"
              :max="2147483647"
              :step="1"
              placeholder="0"
            />
          </KycpFieldWrapper>
          <code>Value: {{ examples.integer || 0 }}</code>
        </div>

        <!-- Decimal -->
        <div class="example">
          <h3>Decimal (precision 18, scale 2)</h3>
          <KycpFieldWrapper label="Annual Revenue">
            <KycpInput 
              v-model="examples.decimal" 
              type="number"
              :step="0.01"
              placeholder="0.00"
              @input="enforceDecimalScale"
            />
          </KycpFieldWrapper>
          <code>Value: {{ examples.decimal || 0 }}</code>
        </div>

        <!-- Date -->
        <div class="example">
          <h3>Date (DD/MM/YYYY)</h3>
          <KycpFieldWrapper label="Date of Incorporation" :required="true">
            <KycpInput 
              v-model="examples.date" 
              type="date"
              placeholder="DD/MM/YYYY"
            />
          </KycpFieldWrapper>
          <code>Value: {{ examples.date || 'not set' }}</code>
        </div>

        <!-- Lookup -->
        <div class="example">
          <h3>Lookup (Dropdown only, stores option code)</h3>
          <KycpFieldWrapper label="Country of Registration" :required="true">
            <KycpSelect 
              v-model="examples.lookup"
              :options="countryOptions"
              placeholder="Select country..."
            />
          </KycpFieldWrapper>
          <code>Selected code: {{ examples.lookup || 'none' }}</code>
          <p class="note">
            <strong>Note:</strong> KYCP does not have radio buttons. All single-select fields use Lookup with dropdown presentation.
            The component always stores and emits the option code, not the label.
          </p>
        </div>
      </section>

      <!-- Non-Input Components -->
      <section id="non-input" class="component-section">
        <h2>Non-Input Components</h2>
        <p class="section-description">
          Components that provide structure and interaction but don't capture data.
        </p>

        <!-- Statement -->
        <div class="example">
          <h3>Statement</h3>
          <KycpStatement 
            html="<strong>Important:</strong> Please ensure all information is accurate. 
                  For more details, visit <a href='#'>our guidelines</a>."
          />
          <p class="note">Supports simple rich text and hyperlinks. No data captured.</p>
        </div>

        <!-- Divider/Title -->
        <div class="example">
          <h3>Divider/Title</h3>
          <KycpDivider title="Section 2: Financial Information" />
          <p>Content after the divider...</p>
          <KycpDivider />
          <p>Content after a simple line divider...</p>
          <p class="note">Visual structure only. No data captured.</p>
        </div>

        <!-- Button -->
        <div class="example">
          <h3>Button</h3>
          <div style="display: flex; gap: 12px; align-items: center;">
            <KycpButton 
              variant="primary"
              label="Submit Application"
              scriptId="submit_app"
              @trigger="handleScript"
            />
            <KycpButton 
              variant="secondary"
              label="Save Draft"
              scriptId="save_draft"
              @trigger="handleScript"
            />
            <KycpButton 
              variant="primary"
              label="Read-only Mode"
              scriptId="test"
              :readonly="true"
            />
            <span style="font-size: 14px; color: var(--kycp-gray-600);">← Does nothing when readonly</span>
          </div>
          <code v-if="lastScript">Last triggered: {{ lastScript }}</code>
          <p class="note">Triggers predefined scripts. In prototypes, emit scriptId and no-op. Respects read-only states.</p>
        </div>
      </section>

      <!-- Complex Groups -->
      <section id="complex" class="component-section">
        <h2>Complex Groups (Repeaters)</h2>
        <p class="section-description">
          Equivalent to KYCP Complex Type. For repeatable sets of related fields only (ID docs, addresses, shareholders).
          One level deep - no nested repeaters. Data stored as array of row objects under the group key.
        </p>

        <div class="example">
          <h3>Example: Identification Documents</h3>
          <KycpRepeater
            v-model="examples.documents"
            item-label="Document"
            add-label="Document Details"
            title-field="type"
          >
            <template #item="{ item }">
              <div style="display: grid; gap: 12px;">
                <span><strong>Type:</strong> {{ item.type }}</span>
                <span><strong>Number:</strong> {{ item.number }}</span>
                <span><strong>Expiry:</strong> {{ item.expiry || 'N/A' }}</span>
              </div>
            </template>
            
            <template #form="{ item, save, cancel }">
              <div style="display: grid; gap: 16px;">
                <KycpFieldWrapper label="Document Type" :required="true">
                  <KycpSelect 
                    v-model="item.type"
                    :options="docTypeOptions"
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
          
          <code style="white-space: pre;">Data structure:
{
  "documents": {{ JSON.stringify(examples.documents, null, 2) }}
}</code>
        </div>
      </section>

      <!-- Platform Limits -->
      <section id="limits" class="component-section">
        <h2>KYCP Platform Limits</h2>
        <p class="section-description">Default limits enforced by components to match KYCP platform.</p>
        
        <table class="limits-table">
          <thead>
            <tr>
              <th>Data Type</th>
              <th>Limit</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>string</strong></td>
              <td>1,024 characters</td>
              <td>Single-line text input</td>
            </tr>
            <tr>
              <td><strong>freeText</strong></td>
              <td>8,192 characters</td>
              <td>Multi-line textarea</td>
            </tr>
            <tr>
              <td><strong>integer</strong></td>
              <td>0 to 2,147,483,647</td>
              <td>Whole numbers only</td>
            </tr>
            <tr>
              <td><strong>decimal</strong></td>
              <td>Precision 18, Scale 2</td>
              <td>Max 18 digits total, 2 after decimal</td>
            </tr>
            <tr>
              <td><strong>date</strong></td>
              <td>DD/MM/YYYY format</td>
              <td>Real date validation, zero-padded</td>
            </tr>
            <tr>
              <td><strong>lookup</strong></td>
              <td>Stores option code</td>
              <td>Always dropdown, no radio buttons</td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Visibility & Rights -->
      <section id="visibility" class="component-section">
        <h2>Visibility & Status Rights</h2>
        
        <div class="info-block">
          <h3>Visibility Rules</h3>
          <ul>
            <li>Conditions compare another field's keyname using <strong>equals</strong> or <strong>not-equals</strong></li>
            <li>Multiple conditions act as <strong>AND</strong></li>
            <li>May target single fields or whole groups</li>
            <li>If a required field is hidden, it does not block submission</li>
            <li>Re-validate when hidden fields become visible</li>
          </ul>
        </div>

        <div class="info-block">
          <h3>Status-Based Rights</h3>
          <ul>
            <li>Per status: <strong>invisible</strong>, <strong>read</strong>, <strong>write</strong></li>
            <li>A <strong>global</strong> mode can blanket-apply unless specifically overridden</li>
            <li>When application is read-only or closed, all fields render read-only</li>
            <li>Buttons do nothing (no-op) in read-only states</li>
          </ul>
        </div>

        <div class="info-block">
          <h3>Internal/System Items</h3>
          <p>Items marked internal or system in admin are not exposed to client staging, even if grouped.</p>
        </div>
      </section>

      <!-- Modal (Prototype Only) -->
      <section id="modal" class="component-section">
        <h2>Modal (Prototype Only)</h2>
        <p class="section-description">
          <strong class="warning">⚠️ Prototype scaffolding only</strong> - KYCP does not define a generic modal component.
          Used for upload dialogs and confirmations in prototypes.
        </p>
        
        <div class="example">
          <KycpButton variant="primary" @click="showModal = true">Open Example Modal</KycpButton>
          
          <KycpModal 
            v-model="showModal" 
            title="Upload Document"
            icon="↑"
          >
            <p>Modal content for document upload UI...</p>
            
            <template #footer>
              <KycpButton variant="secondary" @click="showModal = false">Cancel</KycpButton>
              <KycpButton variant="primary" @click="showModal = false">Upload</KycpButton>
            </template>
          </KycpModal>
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
import KycpStatement from '~/components/kycp/base/KycpStatement.vue'
import KycpDivider from '~/components/kycp/base/KycpDivider.vue'
import KycpRepeater from '~/components/kycp/base/KycpRepeater.vue'
import KycpModal from '~/components/kycp/base/KycpModal.vue'
import KycpButton from '~/components/kycp/base/KycpButton.vue'

// Example data
const showModal = ref(false)
const lastScript = ref('')

const examples = ref({
  string: '',
  freeText: '',
  integer: null,
  decimal: null,
  date: '',
  lookup: '',
  documents: [],
  fundName: '',
  fundType: ''
})

// Fund type description matching screenshot
const fundTypeDescription = `RBSI target sub-sector includes Private Equity, Private Debt, Private Equity Real Estate and other property funds, Infrastructure and Renewables, Fund of Funds.<br>
MSB services can include the below activity(/ies):<br>
<ul>
  <li><strong>Currency Dealing:</strong> FX broking where 3rd party payments can be made. Not to be confused with wholesale trading activity.</li>
  <li><strong>Bureaux de change:</strong> physical exchange of foreign bank notes over the counter.</li>
  <li><strong>Cheque Cashing:</strong> the exchange of cheques for cash.</li>
  <li><strong>Money Remittance:</strong> electronic transfer of money.</li>
  <li><strong>Monetary Instruments:</strong> e-money instruments, such as e-wallets or prepaid cards.</li>
  <li><strong>Payment Service Provider (PSP):</strong> facilitation of access to online payment gateways or online banking, where the transfer of funds occurs.</li>
</ul>`

// Options
const countryOptions = [
  { value: 'GB', label: 'United Kingdom' },
  { value: 'US', label: 'United States' },
  { value: 'DE', label: 'Germany' },
  { value: 'FR', label: 'France' }
]

const fundTypeOptions = [
  { value: 'PE', label: 'Private Equity' },
  { value: 'PD', label: 'Private Debt' },
  { value: 'RE', label: 'Real Estate' },
  { value: 'INFRA', label: 'Infrastructure' },
  { value: 'FOF', label: 'Fund of Funds' },
  { value: 'OTHER', label: 'Other' }
]

const docTypeOptions = [
  { value: 'PASS', label: 'Passport' },
  { value: 'DRVL', label: 'Driver License' },
  { value: 'IDCD', label: 'ID Card' }
]

// Handlers
const enforceDecimalScale = (e: Event) => {
  const input = e.target as HTMLInputElement
  const value = input.value
  if (value.includes('.')) {
    const parts = value.split('.')
    if (parts[1]?.length > 2) {
      input.value = `${parts[0]}.${parts[1].slice(0, 2)}`
      examples.value.decimal = parseFloat(input.value)
    }
  }
}

const handleScript = (scriptId: string) => {
  lastScript.value = scriptId
  console.log('Script triggered:', scriptId)
}
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
  border-bottom-color: var(--color-link);
}

.library-content {
  padding: 48px 32px;
  max-width: 1200px;
  margin: 0 auto;
}

.component-section {
  margin-bottom: 64px;
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
  line-height: 1.5;
}

.example {
  background: #f8f9fa;
  padding: 24px;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
  margin-bottom: 24px;
}

.example h3 {
  margin: 0 0 20px;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.example code {
  display: block;
  margin-top: 16px;
  padding: 12px;
  background: var(--color-bg);
  border-radius: 4px;
  font-size: 13px;
  color: var(--color-text-secondary);
  font-family: monospace;
}

.note {
  margin-top: 12px;
  padding: 12px;
  background: var(--kycp-gray-50);
  border-left: 3px solid var(--kycp-primary);
  border-radius: 3px;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.limits-table {
  width: 100%;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
}

.limits-table th {
  background: var(--color-bg);
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: var(--color-text-primary);
  border-bottom: 1px solid var(--color-border);
}

.limits-table td {
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-secondary);
}

.limits-table tr:last-child td {
  border-bottom: none;
}

.info-block {
  background: var(--color-surface);
  padding: 24px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  margin-bottom: 24px;
}

.info-block h3 {
  margin: 0 0 16px;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.info-block ul {
  margin: 0;
  padding-left: 24px;
  line-height: 1.8;
  color: var(--color-text-secondary);
}

.info-block p {
  margin: 0;
  color: var(--color-text-secondary);
  line-height: 1.5;
}

.warning {
  color: var(--kycp-error);
}
</style>