import { writable } from 'svelte/store';

const createDialogStore = () => {
    const { subscribe, set, update } = writable({
        showDialog: false,
        message: '',
        title: '',
        confirmText: 'common_yes',
        cancelText: 'common_no',
        barrierDismiss: true,
        messageTextAlign: 'text-center',
        showCancel: true,
        onConfirm: () => {},
        onCancel: () => {}
    });
    
    const onCancelDefault = () => {
        update(state => ({ ...state, showDialog: false }));
    };

    return {
        subscribe,
        openDialog: (
            { 
                message = '', 
                title = '', 
                confirmText = 'common_yes',
                cancelText = 'common_no',
                barrierDismiss = true,
                messageTextAlign = 'text-center',
                showCancel = true,
                onConfirm = () => {},
                onCancel = onCancelDefault 
            } = {}) => {
            update(state => ({
                ...state,
                showDialog: true,
                message,
                title,
                confirmText,
                cancelText,
                barrierDismiss,
                messageTextAlign,
                showCancel,
                onConfirm,
                onCancel
            }));
        },
        closeDialog: () => {
            set({
                showDialog: false,
                message: '',
                title: '',
                confirmText: 'common_yes',
                cancelText: 'common_no',
                barrierDismiss: true,
                messageTextAlign: 'text-center',
                showCancel: true,
                onConfirm: () => {},
                onCancel: () => {}
            });
        }
    };
};

export const dialog = createDialogStore();