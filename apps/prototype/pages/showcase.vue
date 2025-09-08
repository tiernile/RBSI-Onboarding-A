<template>
  <div class="showcase">
    <header class="showcase-header">
      <div class="showcase-header-content">
        <NuxtLink to="/" class="back-link">← Mission Control</NuxtLink>
        <h1>KYCP Component Showcase</h1>
        <p class="subtitle">Interactive component library for RBSI forms</p>
      </div>
    </header>

    <nav class="showcase-nav">
      <a href="#inputs" class="nav-link">Inputs</a>
      <a href="#selections" class="nav-link">Selections</a>
      <a href="#layout" class="nav-link">Layout</a>
      <a href="#feedback" class="nav-link">Feedback</a>
    </nav>

    <main class="showcase-content">
      <!-- Input Components -->
      <section id="inputs" class="component-section">
        <h2>Input Components</h2>
        
        <div class="component-demo">
          <h3>KycpInput</h3>
          <div class="demo-panel">
            <KycpFieldWrapper
              id="demo-input"
              label="Name"
              :required="true"
              help="Enter your full legal name"
              :error="inputError"
            >
              <KycpInput
                id="demo-input"
                v-model="formData.name"
                placeholder="Enter name"
                :error="!!inputError"
                aria-describedby="demo-input-help demo-input-error"
              />
            </KycpFieldWrapper>
          </div>
          <div class="code-panel">
            <pre><code>{{ inputCode }}</code></pre>
          </div>
        </div>

        <div class="component-demo">
          <h3>KycpSelect</h3>
          <div class="demo-panel">
            <KycpFieldWrapper
              id="demo-select"
              label="Entity Type"
              :required="true"
            >
              <KycpSelect
                id="demo-select"
                v-model="formData.entityType"
                :options="entityOptions"
                placeholder="Select entity type"
              />
            </KycpFieldWrapper>
          </div>
          <div class="code-panel">
            <pre><code>{{ selectCode }}</code></pre>
          </div>
        </div>
      </section>

      <!-- Selection Components -->
      <section id="selections" class="component-section">
        <h2>Selection Components</h2>
        
        <div class="component-demo">
          <h3>KycpRadio</h3>
          <div class="demo-panel">
            <KycpFieldWrapper
              label="Validation Type"
              :required="true"
            >
              <KycpRadio
                v-model="formData.validationType"
                :options="validationOptions"
                name="validation-type"
              />
            </KycpFieldWrapper>
          </div>
          <div class="code-panel">
            <pre><code>{{ radioCode }}</code></pre>
          </div>
        </div>
      </section>

      <!-- Layout Components -->
      <section id="layout" class="component-section">
        <h2>Layout Components</h2>
        
        <div class="component-demo">
          <h3>KycpFieldGroup</h3>
          <div class="demo-panel">
            <KycpFieldGroup 
              title="REQUIRED GROUP"
              subtitle="PROGRAM: Corporate Services"
            >
              <KycpFieldWrapper
                id="group-name"
                label="Name"
                :required="true"
              >
                <KycpInput
                  id="group-name"
                  v-model="formData.groupName"
                  placeholder="Test"
                />
              </KycpFieldWrapper>
              
              <KycpFieldWrapper
                id="group-entity"
                label="Entity Type"
              >
                <KycpSelect
                  id="group-entity"
                  v-model="formData.groupEntity"
                  :options="['UBO', 'LLC', 'Partnership']"
                  placeholder="Select type"
                />
              </KycpFieldWrapper>

              <KycpFieldWrapper
                label="Validation Type"
              >
                <KycpRadio
                  v-model="formData.groupValidation"
                  :options="['At least 1 filled', 'All required', 'Optional']"
                  name="group-validation"
                />
              </KycpFieldWrapper>
            </KycpFieldGroup>
          </div>
          <div class="code-panel">
            <pre><code>{{ fieldGroupCode }}</code></pre>
          </div>
        </div>
      </section>

      <!-- Feedback Components -->
      <section id="feedback" class="component-section">
        <h2>Feedback Components</h2>
        
        <div class="component-demo">
          <h3>KycpTag</h3>
          <div class="demo-panel">
            <div class="tags-container">
              <KycpTag 
                v-for="tag in tags" 
                :key="tag"
                :label="tag"
                :removable="true"
                @remove="removeTag(tag)"
              />
            </div>
            <button @click="addTag" class="add-tag-btn">+ Add Tag</button>
          </div>
          <div class="code-panel">
            <pre><code>{{ tagCode }}</code></pre>
          </div>
        </div>
      </section>

      <!-- Component States -->
      <section class="component-section">
        <h2>Component States</h2>
        <div class="states-grid">
          <div class="state-demo">
            <h4>Default</h4>
            <KycpInput placeholder="Default state" />
          </div>
          <div class="state-demo">
            <h4>Focused</h4>
            <KycpInput placeholder="Click to focus" />
          </div>
          <div class="state-demo">
            <h4>Error</h4>
            <KycpInput placeholder="Error state" :error="true" />
          </div>
          <div class="state-demo">
            <h4>Disabled</h4>
            <KycpInput placeholder="Disabled" :disabled="true" />
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import KycpInput from '~/components/kycp/base/KycpInput.vue'
import KycpSelect from '~/components/kycp/base/KycpSelect.vue'
import KycpRadio from '~/components/kycp/base/KycpRadio.vue'
import KycpFieldWrapper from '~/components/kycp/base/KycpFieldWrapper.vue'
import KycpFieldGroup from '~/components/kycp/base/KycpFieldGroup.vue'
import KycpTag from '~/components/kycp/base/KycpTag.vue'

// Import the CSS
import '~/assets/kycp-design.css'

// Demo data
const formData = ref({
  name: '',
  entityType: '',
  validationType: 'At least 1 filled',
  groupName: 'Test',
  groupEntity: 'UBO',
  groupValidation: 'At least 1 filled'
})

const inputError = ref('')
const entityOptions = ['Limited Partnership', 'Corporation', 'LLC', 'Trust']
const validationOptions = ['At least 1 filled', 'All required', 'Optional']

const tags = ref(['GENSurname', 'GENName', 'GENCountry'])

const removeTag = (tag: string) => {
  const index = tags.value.indexOf(tag)
  if (index > -1) {
    tags.value.splice(index, 1)
  }
}

const addTag = () => {
  const newTag = `Field${tags.value.length + 1}`
  tags.value.push(newTag)
}

// Code examples
const inputCode = `<KycpFieldWrapper
  id="name-field"
  label="Name"
  :required="true"
  help="Enter your full legal name"
  :error="error"
>
  <KycpInput
    id="name-field"
    v-model="formData.name"
    placeholder="Enter name"
    :error="!!error"
  />
</KycpFieldWrapper>`

const selectCode = `<KycpSelect
  v-model="formData.entityType"
  :options="entityOptions"
  placeholder="Select entity type"
/>`

const radioCode = `<KycpRadio
  v-model="formData.validationType"
  :options="validationOptions"
  name="validation-type"
/>`

const fieldGroupCode = `<KycpFieldGroup 
  title="REQUIRED GROUP"
  subtitle="PROGRAM: Corporate Services"
>
  <!-- Field components here -->
</KycpFieldGroup>`

const tagCode = `<KycpTag 
  :label="tagName"
  :removable="true"
  @remove="handleRemove"
/>`
</script>

<style scoped>
.showcase {
  min-height: 100vh;
  background: #f8f9fa;
}

.showcase-header {
  background: white;
  border-bottom: 1px solid #e1e4e8;
  padding: 24px 0;
}

.showcase-header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.back-link {
  color: #0969da;
  text-decoration: none;
  font-size: 14px;
  margin-bottom: 16px;
  display: inline-block;
}

.back-link:hover {
  text-decoration: underline;
}

.showcase-header h1 {
  margin: 8px 0;
  font-size: 32px;
  font-weight: 600;
  color: #0d1117;
}

.subtitle {
  margin: 0;
  color: #57606a;
  font-size: 16px;
}

.showcase-nav {
  background: white;
  border-bottom: 1px solid #e1e4e8;
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 10;
}

.nav-link {
  display: inline-block;
  padding: 16px 24px;
  color: #57606a;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  border-bottom: 2px solid transparent;
  transition: all 150ms ease;
}

.nav-link:hover {
  color: #0969da;
  border-bottom-color: #0969da;
}

.showcase-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
}

.component-section {
  margin-bottom: 48px;
}

.component-section h2 {
  font-size: 24px;
  font-weight: 600;
  color: #0d1117;
  margin-bottom: 24px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e1e4e8;
}

.component-demo {
  background: white;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 24px;
}

.component-demo h3 {
  margin: 0;
  padding: 16px 24px;
  background: #f6f8fa;
  border-bottom: 1px solid #e1e4e8;
  font-size: 16px;
  font-weight: 600;
  color: #0d1117;
}

.demo-panel {
  padding: 24px;
}

.code-panel {
  background: #f6f8fa;
  border-top: 1px solid #e1e4e8;
  padding: 16px 24px;
  overflow-x: auto;
}

.code-panel pre {
  margin: 0;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
  font-size: 13px;
  line-height: 1.5;
  color: #0d1117;
}

.code-panel code {
  white-space: pre;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.add-tag-btn {
  padding: 6px 12px;
  background: #f6f8fa;
  border: 1px solid #d0d7de;
  border-radius: 6px;
  font-size: 14px;
  color: #0969da;
  cursor: pointer;
  transition: all 150ms ease;
}

.add-tag-btn:hover {
  background: #f3f4f6;
  border-color: #0969da;
}

.states-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  background: white;
  padding: 24px;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
}

.state-demo h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: #57606a;
}
</style>