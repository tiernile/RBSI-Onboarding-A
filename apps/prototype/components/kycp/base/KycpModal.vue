<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="kycp-modal-overlay" @click="handleOverlayClick">
        <div class="kycp-modal" @click.stop>
          <div class="kycp-modal__header">
            <h3 class="kycp-modal__title">
              <span v-if="icon" class="kycp-modal__icon">{{ icon }}</span>
              {{ title }}
            </h3>
            <button
              type="button"
              class="kycp-modal__close"
              @click="close"
              aria-label="Close modal"
            >
              ×
            </button>
          </div>
          
          <div class="kycp-modal__content">
            <slot></slot>
          </div>
          
          <div v-if="$slots.footer" class="kycp-modal__footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
interface Props {
  modelValue: boolean
  title: string
  icon?: string
  closeOnOverlay?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  closeOnOverlay: true
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const close = () => {
  emit('update:modelValue', false)
}

const handleOverlayClick = () => {
  if (props.closeOnOverlay) {
    close()
  }
}
</script>

<style scoped>
.kycp-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.kycp-modal {
  background: var(--kycp-white);
  border-radius: 8px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.kycp-modal__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--kycp-section-border);
}

.kycp-modal__title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--kycp-gray-900);
  display: flex;
  align-items: center;
  gap: 8px;
}

.kycp-modal__icon {
  font-size: 20px;
}

.kycp-modal__close {
  width: 32px;
  height: 32px;
  padding: 0;
  background: transparent;
  border: none;
  color: var(--kycp-gray-600);
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
  transition: color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.kycp-modal__close:hover {
  color: var(--kycp-gray-900);
}

.kycp-modal__content {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.kycp-modal__footer {
  padding: 16px 24px;
  border-top: 1px solid var(--kycp-section-border);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* Transition animations */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .kycp-modal,
.modal-leave-active .kycp-modal {
  transition: transform 0.3s ease;
}

.modal-enter-from .kycp-modal {
  transform: scale(0.9);
}

.modal-leave-to .kycp-modal {
  transform: scale(0.9);
}
</style>